import os
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from datetime import datetime, timezone
from api_service.app import app

# ใช้ไฟล์ .env.test
from dotenv import load_dotenv
load_dotenv()

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("DB_NAME", "ipa2025_test")
    mongo = MongoClient(mongo_uri)
    db = mongo[db_name]
    collection = db["interface_status"]
    collection.delete_many({})  # ล้างข้อมูลก่อน

    # ใส่ mock ข้อมูล
    now = datetime.now(timezone.utc)
    data = [
        {
            "router_id": "r1",
            "router_ip": "192.168.1.1",
            "interfaces": [
                { "interface": "Gig0/0", "status": "up", "protocol": "up" }
                        ],
            "created_at": now
        },
        {
            "router_id": "r2",
            "router_ip": "192.168.1.2",
            "interfaces": [
                { "interface": "Gig0/0", "status": "up", "protocol": "up" }
                        ],
            "created_at": now
        },
    ]
    collection.insert_many(data)

    yield  # รันเทสต์

    # ทำความสะอาดหลังเทสต์
    collection.delete_many({})
    mongo.close()

def test_get_all_interfaces():
    response = client.get("/api/interfaces")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert any(d["router_ip"] == "192.168.1.1" for d in data)
    assert any(d["router_ip"] == "192.168.1.2" for d in data)


def test_get_interfaces_by_ip():
    response = client.get("/api/interfaces/192.168.1.1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["router_ip"] == "192.168.1.1"
    assert "interfaces" in data[0]
    assert isinstance(data[0]["interfaces"], list)
    assert "interface" in data[0]["interfaces"][0]
