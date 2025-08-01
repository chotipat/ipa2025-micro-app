from unittest.mock import patch, MagicMock
from worker.mongo_client import save_interface_data


@patch("worker.mongo_client.MongoClient")
def test_save_interface_data(mock_mongo_client):
    # Mock db.collection.insert_one
    mock_collection = MagicMock()
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection  # db["interface_status"]

    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db  # client[DB_NAME]

    mock_mongo_client.return_value = mock_client  # MongoClient(...) -> mock_client

    router_id = "r1"
    router_ip = "192.168.1.1"
    interfaces = [{"intf": "Gig0/0", "status": "up"}]

    save_interface_data(router_id, router_ip, interfaces)

    mock_collection.insert_one.assert_called_once()
    assert mock_collection.insert_one.call_count == 1
    args, kwargs = mock_collection.insert_one.call_args
    inserted_data = args[0]

    assert inserted_data["router_id"] == router_id
    assert inserted_data["router_ip"] == router_ip
    assert inserted_data["interfaces"] == interfaces
    assert "created_at" in inserted_data
