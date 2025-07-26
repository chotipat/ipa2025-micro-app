from apscheduler.schedulers.blocking import BlockingScheduler
from database import routers_collection
from rabbitmq import channel
import json

def get_interface_status():
    print("⏰ Running scheduled job")
    routers = routers_collection.find()
    for router in routers:
        payload = {
            "router_id": str(router["_id"]),
            "router_info": {
                "device_type": "cisco_ios",
                "host": router["ip"],
                "username": router["username"],
                "password": router["password"],
            },
        }
        try: 
            channel.basic_publish(
                exchange="",
                routing_key="router_jobs",
                body=json.dumps(payload),
            )
            print(f"[✓] Published payload for {router['ip']}")
        except Exception as e:
            print(f"[!] Failed to publish for {router['ip']}: {e}")

def run_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(get_interface_status, "interval", minutes=1)
    print("📅 Scheduler started")
    scheduler.start()

if __name__ == "__main__":
    run_scheduler()
