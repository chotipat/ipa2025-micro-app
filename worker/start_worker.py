# worker/worker.py
import pika
import time
import os
from worker.handler import callback

print(">> worker.py started <<")

rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

for i in range(10):
    try:
        print(f"[ ] Connecting to RabbitMQ (attempt {i+1})...")
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
        parameters = pika.ConnectionParameters(rabbitmq_host, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        print("[✓] Connected to RabbitMQ")
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[!] Connection failed: {e}")
        time.sleep(5)
else:
    print("[x] Could not connect to RabbitMQ after 10 attempts. Exiting.")
    exit(1)

channel = connection.channel()
channel.queue_declare(queue="router_jobs")
channel.basic_consume(queue="router_jobs", on_message_callback=callback, auto_ack=True)

print(" [*] Worker waiting for messages...")
channel.basic_qos(prefetch_count=1)
channel.start_consuming()
