from fastapi import FastAPI
from fastapi.responses import Response
from pymongo import MongoClient
from bson.json_util import dumps
#from bson.objectid import ObjectId

app = FastAPI()

client = MongoClient("mongodb://mongo:27017/")
db = client["ipa2025"]
interfaces_collection = db["interface_status"]

@app.get("/api/interfaces")
def get_all_interfaces():
    data = list(interfaces_collection.find({}, {"_id": 0}))
    return Response(content=dumps(data), media_type="application/json")

@app.get("/api/interfaces/{ip}")
def get_interfaces_by_ip(ip: str):
    data = list(interfaces_collection.find({"router_ip": ip}, {"_id": 0}))
    return Response(content=dumps(data), media_type="application/json")
