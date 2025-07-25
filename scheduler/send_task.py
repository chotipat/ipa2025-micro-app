import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

channel.queue_declare(queue="router_jobs")

channel.basic_publish(exchange="", routing_key="router_jobs", body="192.168.1.44")
print("Sent job for router 192.168.1.44")
connection.close()
