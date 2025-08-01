# worker/handler.py
import json
from worker.parser import parse_interfaces
from worker.router_client import fetch_interface_status
from worker.mongo_client import save_interface_data


def callback(ch, method, properties, body):
    job = json.loads(body.decode())
    router_info = job["router_info"]
    print(f" [x] Received job for router {router_info['host']}")

    try:
        raw_output = fetch_interface_status(router_info)
        interfaces = parse_interfaces(raw_output)
        save_interface_data(job["router_id"], router_info["host"], interfaces)
        print(f" [✓] Stored interface status for {router_info['host']}")
    except Exception as e:
        print(f" [!] Error: {e}")
