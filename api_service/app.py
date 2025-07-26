from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

app = FastAPI()

client = MongoClient("mongodb://mongo:27017/")
db = client["ipa2025"]
interfaces_collection = db["interface_status"]

tz_bangkok = timezone(timedelta(hours=7))

@app.get("/api/interfaces")
def get_all_interfaces():
    pipeline = [
        {"$sort": {"created_at": -1}},  
        {"$group": {
            "_id": "$router_ip",
            "latest": {"$first": "$$ROOT"}
        }},
        {"$replaceRoot": {"newRoot": "$latest"}},
        {"$project": {"_id": 0}}
    ]
    data = list(interfaces_collection.aggregate(pipeline))

    for doc in data:
        if "created_at" in doc and isinstance(doc["created_at"], datetime):
            doc["created_at"] = doc["created_at"].astimezone(tz_bangkok).strftime("%Y-%m-%d %H:%M:%S")

    return JSONResponse(content=data)

@app.get("/api/interfaces/{ip}")
def get_interfaces_by_ip(ip: str):
    data = list(interfaces_collection.find({"router_ip": ip}, {"_id": 0}))

    for doc in data:
        if "created_at" in doc and isinstance(doc["created_at"], datetime):
            doc["created_at"] = doc["created_at"].astimezone(tz_bangkok).strftime("%Y-%m-%d %H:%M:%S")

    return JSONResponse(content=data)
