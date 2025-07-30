from worker.mongo_client import save_interface_data
from pymongo import MongoClient
from datetime import datetime
import time
import os
from dotenv import load_dotenv

def test_save_interface_data_integration():
    router_id = "test_router_1"
    router_ip = "192.168.100.1"
    interfaces = [{"intf": "Gig0/0", "status": "up"}]

    save_interface_data(router_id, router_ip, interfaces)

    env_file = os.getenv("ENV_FILE", ".env.test")
    load_dotenv(dotenv_path=env_file)

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "ipa2025_test")
    mongo = MongoClient(MONGO_URI)
    db = mongo[DB_NAME]
    collection = db["interface_status"]

    time.sleep(1)

    doc = collection.find_one({"router_id": router_id, "router_ip": router_ip})

    assert doc is not None
    assert doc["interfaces"] == interfaces
    assert isinstance(doc["created_at"], datetime)

    collection.delete_many({"router_id": router_id})
