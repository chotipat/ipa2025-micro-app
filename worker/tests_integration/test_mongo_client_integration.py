from worker.mongo_client import save_interface_data
from pymongo import MongoClient
from datetime import datetime
import time

def test_save_interface_data_integration():
    # 1. เตรียมข้อมูลทดสอบ
    router_id = "test_router_1"
    router_ip = "192.168.100.1"
    interfaces = [{"intf": "Gig0/0", "status": "up"}]

    # 2. เรียกฟังก์ชันจริง
    save_interface_data(router_id, router_ip, interfaces)

    # 3. เช็คว่า MongoDB มีข้อมูลที่เพิ่งบันทึกไป
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ipa2025"]
    collection = db["interface_status"]

    # รอเล็กน้อยให้ MongoDB เขียนข้อมูลเสร็จ
    time.sleep(1)

    doc = collection.find_one({"router_id": router_id, "router_ip": router_ip})

    assert doc is not None
    assert doc["interfaces"] == interfaces
    assert isinstance(doc["created_at"], datetime)

    # 4. ลบข้อมูลออกหลังจบ (เพื่อความสะอาด)
    collection.delete_many({"router_id": router_id})
