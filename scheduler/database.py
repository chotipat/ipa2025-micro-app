from pymongo import MongoClient
from dotenv import load_dotenv
import os

env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=env_file)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
DB_NAME = os.getenv("DB_NAME", "ipa2025")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
routers_collection = db["routers"]
