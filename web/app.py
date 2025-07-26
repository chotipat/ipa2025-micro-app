from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from bson import ObjectId
import requests

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client["ipa2025"]
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
    print(interfaces)
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
