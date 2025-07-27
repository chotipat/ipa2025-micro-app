from unittest.mock import patch, MagicMock
from worker.mongo_client import save_interface_data

@patch("worker.mongo_client.MongoClient")  # 👈 mock MongoClient ใน module นี้
def test_save_interface_data(mock_mongo):
    # Step 1: เตรียม mock collection
    mock_collection = MagicMock()
    mock_db = {"interface_status": mock_collection}
    mock_mongo.return_value = {"ipa2025": mock_db}

    # Step 2: mock datetime.now(UTC)
    router_id = "r1"
    router_ip = "192.168.1.1"
    interfaces = [{"intf": "Gig0/0", "status": "up"}]

    # เรียกฟังก์ชันจริง (ที่ใช้ mock อยู่แล้ว)
    save_interface_data(router_id, router_ip, interfaces)

    # Step 3: ตรวจสอบว่า insert_one ถูกเรียกหนึ่งครั้ง และข้อมูลถูกต้องบางส่วน
    assert mock_collection.insert_one.call_count == 1
    args, kwargs = mock_collection.insert_one.call_args
    inserted_data = args[0]

    assert inserted_data["router_id"] == router_id
    assert inserted_data["router_ip"] == router_ip
    assert inserted_data["interfaces"] == interfaces
    assert "created_at" in inserted_data
