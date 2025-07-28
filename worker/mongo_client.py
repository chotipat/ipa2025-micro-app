# worker/mongo_client.py
from pymongo import MongoClient
from datetime import datetime, UTC
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)



def save_interface_data(router_id, router_ip, interfaces):
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
    mongo = MongoClient(MONGO_URI)
    db = mongo["ipa2025"]
    collection = db["interface_status"]
    data = {
        "router_id": router_id,
        "router_ip": router_ip,
        "created_at": datetime.now(UTC),
        "interfaces": interfaces
    }
    collection.insert_one(data)
