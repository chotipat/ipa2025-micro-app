import pika
import time

for i in range(10):
    try:
        print(f"[ ] Connecting to RabbitMQ from scheduler (attempt {i+1})...")
        credentials = pika.PlainCredentials("guest", "guest")
        parameters = pika.ConnectionParameters("rabbitmq", credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        print("[✓] Connected to RabbitMQ from scheduler")
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[!] Connection failed: {e}")
        time.sleep(5)
else:
    print("[x] Could not connect to RabbitMQ from scheduler after 5 attempts. Exiting.")
    exit(1)

channel = connection.channel()
channel.queue_declare(queue="router_jobs")
