from unittest.mock import patch
from worker.handler import callback
from pytest import CaptureFixture
import json


@patch("worker.handler.save_interface_data")
@patch("worker.handler.parse_interfaces")
@patch("worker.handler.fetch_interface_status")
def test_callback_success(mock_fetch, mock_parse, mock_save):
    # Mock return values
    mock_fetch.return_value = "raw"
    mock_parse.return_value = [{"interface": "Gig0/0", "status": "up"}]

    # Prepare dummy message body
    job = {
        "router_id": "r1",
        "router_info": {
            "host": "192.168.1.1",
            "device_type": "cisco_ios",
            "username": "admin",
            "password": "admin",
        },
    }
    body = json.dumps(job).encode()

    # Run
    callback(ch=None, method=None, properties=None, body=body)

    # Assertions
    mock_fetch.assert_called_once_with(job["router_info"])
    mock_parse.assert_called_once_with("raw")
    mock_save.assert_called_once_with("r1", "192.168.1.1", mock_parse.return_value)


@patch("worker.handler.save_interface_data")
@patch("worker.handler.parse_interfaces")
@patch("worker.handler.fetch_interface_status")
def test_callback_error_in_fetch(
    mock_fetch, mock_parse, mock_save, capsys: CaptureFixture
):
    mock_fetch.side_effect = Exception("connection failed")

    job = {
        "router_id": "r1",
        "router_info": {
            "host": "192.168.1.1",
            "device_type": "cisco_ios",
            "username": "admin",
            "password": "admin",
        },
    }
    body = json.dumps(job).encode()

    callback(ch=None, method=None, properties=None, body=body)

    mock_parse.assert_not_called()
    mock_save.assert_not_called()

    out, err = capsys.readouterr()
    assert "connection failed" in out


@patch("worker.handler.save_interface_data")
@patch("worker.handler.parse_interfaces")
@patch("worker.handler.fetch_interface_status")
def test_callback_error_in_parse(
    mock_fetch, mock_parse, mock_save, capsys: CaptureFixture
):
    mock_fetch.return_value = "raw data"
    mock_parse.side_effect = Exception("parse error")

    job = {
        "router_id": "r1",
        "router_info": {
            "host": "192.168.1.1",
            "device_type": "cisco_ios",
            "username": "admin",
            "password": "admin",
        },
    }
    body = json.dumps(job).encode()

    callback(ch=None, method=None, properties=None, body=body)

    mock_fetch.assert_called_once()
    mock_parse.assert_called_once_with("raw data")
    mock_save.assert_not_called()  # ✅ เพราะ parse พัง จึงไม่ save

    out, err = capsys.readouterr()
    assert "parse error" in out


@patch("worker.handler.save_interface_data")
@patch("worker.handler.parse_interfaces")
@patch("worker.handler.fetch_interface_status")
def test_callback_error_in_save(
    mock_fetch, mock_parse, mock_save, capsys: CaptureFixture
):
    mock_fetch.return_value = "raw data"
    mock_parse.return_value = [{"intf": "Gig0/0", "status": "up"}]
    mock_save.side_effect = Exception("mongo error")

    job = {
        "router_id": "r1",
        "router_info": {
            "host": "192.168.1.1",
            "device_type": "cisco_ios",
            "username": "admin",
            "password": "admin",
        },
    }
    body = json.dumps(job).encode()

    callback(ch=None, method=None, properties=None, body=body)

    mock_fetch.assert_called_once()
    mock_parse.assert_called_once_with("raw data")
    mock_save.assert_called_once()

    out, err = capsys.readouterr()
    assert "mongo error" in out
