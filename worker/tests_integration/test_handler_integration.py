import os
import json
from pymongo import MongoClient
from worker.handler import callback

def test_callback_real_router_and_mongo():
    
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "ipa2025_test")

    router_info = {
        "device_type": "cisco_ios",
        "host": os.getenv("TEST_ROUTER_IP"),
        "ip": os.getenv("TEST_ROUTER_IP"),
        "username": os.getenv("TEST_ROUTER_USERNAME"),
        "password": os.getenv("TEST_ROUTER_PASSWORD"),
    }

    job = {
        "router_id": "router_test_123",
        "router_info": router_info
    }

    body = json.dumps(job).encode()
    callback(None, None, None, body)

    mongo = MongoClient(MONGO_URI)
    db = mongo[DB_NAME]
    collection = db["interface_status"]

    saved = list(collection.find({"router_id": "router_test_123"}))
    assert len(saved) > 0

    for doc in saved:
        assert doc["router_ip"] == router_info["host"]
        assert isinstance(doc["interfaces"], list)
        assert "interface" in doc["interfaces"][0]
        assert "status" in doc["interfaces"][0]
        assert "protocol" in doc["interfaces"][0]
