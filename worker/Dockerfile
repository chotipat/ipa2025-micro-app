FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pika netmiko==4.2.0 pymongo
CMD ["python3", "-u", "worker.py"]
