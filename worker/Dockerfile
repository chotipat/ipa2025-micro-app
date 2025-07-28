FROM python:3.12-slim
WORKDIR /app
COPY start_worker.py .
COPY . worker/
RUN rm -f /worker/start_worker.py /worker/Dockerfile
RUN pip install --no-cache-dir -r worker/requirements.txt
CMD ["python3", "-u", "start_worker.py"]
