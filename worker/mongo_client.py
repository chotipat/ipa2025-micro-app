# worker/mongo_client.py
from pymongo import MongoClient
from datetime import datetime, UTC
from dotenv import load_dotenv
import os

load_dotenv()

def save_interface_data(router_id, router_ip, interfaces):
    env_file = os.getenv("ENV_FILE", ".env")
    load_dotenv(dotenv_path=env_file)
    
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
    DB_NAME = os.getenv("DB_NAME", "ipa2025")
    
    mongo = MongoClient(MONGO_URI)
    db = mongo[DB_NAME]
    collection = db["interface_status"]
    
    data = {
        "router_id": router_id,
        "router_ip": router_ip,
        "created_at": datetime.now(UTC),
        "interfaces": interfaces
    }
    collection.insert_one(data)
