import pika
from netmiko import ConnectHandler
from pymongo import MongoClient
from datetime import datetime, UTC
import json
import time

print(">> worker.py started <<")

def callback(ch, method, properties, body):
    router_ip = body.decode()
    print(f" [x] Received job for router {router_ip}")

    try:
        connection = ConnectHandler(
            device_type="cisco_ios",
            host=router_ip,
            username="admin",
            password="cisco",  
        )
        output = connection.send_command("show ip interface brief")
        connection.disconnect()

        mongo = MongoClient("mongodb://mongo:27017/")
        db = mongo["ipa2025"]
        collection = db["interface_status"]
        collection.insert_one({
            "router_ip": router_ip,
            "status": output,
            "created_at": datetime.now(UTC),
        })

        print(f" [✓] Stored interface status for {router_ip}")

    except Exception as e:
        print(f" [!] Error: {e}")

for i in range(5):
    try:
        print(f"[ ] Connecting to RabbitMQ (attempt {i+1})...")
        credentials = pika.PlainCredentials("guest", "guest")
        parameters = pika.ConnectionParameters("rabbitmq", credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        print("[✓] Connected to RabbitMQ")
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[!] Connection failed: {e}")
        time.sleep(5)
else:
    print("[x] Could not connect to RabbitMQ after 5 attempts. Exiting.")
    exit(1)

channel = connection.channel()
channel.queue_declare(queue="router_jobs")
channel.basic_consume(queue="router_jobs", on_message_callback=callback, auto_ack=True)

print(" [*] Worker waiting for messages...")
channel.start_consuming()
