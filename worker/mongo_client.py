# worker/mongo_client.py
from pymongo import MongoClient
from datetime import datetime, UTC
import os


def save_interface_data(router_id, router_ip, interfaces):

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
    DB_NAME = os.getenv("DB_NAME", "ipa2025")

    mongo = MongoClient(MONGO_URI)
    db = mongo[DB_NAME]
    collection = db["interface_status"]

    data = {
        "router_id": router_id,
        "router_ip": router_ip,
        "created_at": datetime.now(UTC),
        "interfaces": interfaces,
    }
    collection.insert_one(data)
