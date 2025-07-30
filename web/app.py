from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import requests

env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=env_file)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
DB_NAME = os.getenv("DB_NAME", "ipa2025")

app = Flask(__name__)
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
routers = db["routers"]

API_BASE = "http://api_service:8000"

@app.route("/", methods=["GET"])
def index():
    try:
        res = requests.get(f"{API_BASE}/api/interfaces")
        interfaces = res.json()
    except Exception as e:
        interfaces = []
        print(f"[!] Failed to fetch from api_service: {e}")
    return render_template("index.html", routers=list(routers.find()), interfaces=interfaces)

@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        routers.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    return redirect("/")

@app.route("/delete/<id>", methods=["POST"])
def delete_router(id):
    routers.delete_one({"_id": ObjectId(id)})
    return redirect("/")

@app.route("/router/<ip>")
def router_detail(ip):
    try:
        res = requests.get(f"{API_BASE}/api/interfaces/{ip}")
        interfaces = res.json()
    except Exception as e:
        interfaces = []
        print(f"[!] Failed to fetch interfaces for {ip}: {e}")

    return render_template("router_detail.html", ip=ip, interfaces=interfaces)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
