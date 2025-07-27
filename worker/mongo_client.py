# worker/mongo_client.py
from pymongo import MongoClient
from datetime import datetime, UTC

def save_interface_data(router_id, router_ip, interfaces):
    mongo = MongoClient("mongodb://mongo:27017/")
    db = mongo["ipa2025"]
    collection = db["interface_status"]
    data = {
        "router_id": router_id,
        "router_ip": router_ip,
        "created_at": datetime.now(UTC),
        "interfaces": interfaces
    }
    collection.insert_one(data)
