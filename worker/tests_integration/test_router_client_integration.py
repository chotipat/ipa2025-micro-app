import os
from worker.router_client import fetch_interface_status
from worker.parser import parse_interfaces
from dotenv import load_dotenv

def test_fetch_interface_status_real_router():

    env_file = os.getenv("ENV_FILE", ".env.test")
    load_dotenv(dotenv_path=env_file)

    router_info = {
        "device_type": "cisco_ios",
        "ip": os.getenv("TEST_ROUTER_IP"),
        "username": os.getenv("TEST_ROUTER_USERNAME"),
        "password": os.getenv("TEST_ROUTER_PASSWORD"),
    }

    raw_output = fetch_interface_status(router_info)
    interfaces = parse_interfaces(raw_output)

    assert isinstance(interfaces, list)
    assert len(interfaces) > 0

    for intf in interfaces:
        assert "interface" in intf
        assert "status" in intf
        assert "protocol" in intf
