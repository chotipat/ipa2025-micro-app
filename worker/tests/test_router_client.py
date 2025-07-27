# worker/tests/test_router_client.py
from unittest.mock import patch, MagicMock
from worker.router_client import fetch_interface_status

@patch("worker.router_client.ConnectHandler")
def test_fetch_interface_status(mock_connect):
    mock_conn = MagicMock()
    mock_conn.send_command.return_value = "output here"
    mock_connect.return_value = mock_conn

    dummy_router = {
        "device_type": "cisco_ios",
        "ip": "192.168.1.1",
        "username": "admin",
        "password": "admin"
    }

    result = fetch_interface_status(dummy_router)

    mock_connect.assert_called_once_with(**dummy_router)
    mock_conn.send_command.assert_called_once_with("show ip interface brief")
    mock_conn.disconnect.assert_called_once()
    assert result == "output here"

