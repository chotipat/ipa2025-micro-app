from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["ipa2025"]
routers_collection = db["routers"]
