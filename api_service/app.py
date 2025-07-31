import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
DB_NAME = os.getenv("DB_NAME", "ipa2025")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
interfaces_collection = db["interface_status"]

tz_bangkok = timezone(timedelta(hours=7))

def format_created_at(docs: List[Dict]) -> List[Dict]:
    for doc in docs:
        if "created_at" in doc and isinstance(doc["created_at"], datetime):
            doc["created_at"] = doc["created_at"].astimezone(tz_bangkok).strftime("%Y-%m-%d %H:%M:%S")
    return docs

def get_latest_interface_data(ip: Optional[str] = None) -> List[Dict]:
    pipeline = []

    if ip:
        pipeline.append({"$match": {"router_ip": ip}})

    pipeline += [
        {"$sort": {"created_at": -1}},
        {"$group": {
            "_id": "$router_ip",
            "latest": {"$first": "$$ROOT"}
        }},
        {"$replaceRoot": {"newRoot": "$latest"}},
        {"$project": {"_id": 0}}
    ]

    docs = list(interfaces_collection.aggregate(pipeline))
    return format_created_at(docs)

@app.get("/api/interfaces")
def get_all_interfaces():
    data = get_latest_interface_data()
    return JSONResponse(content=data)

@app.get("/api/interfaces/{ip}")
def get_interfaces_by_ip(ip: str):
    data = get_latest_interface_data(ip)
    return JSONResponse(content=data)
