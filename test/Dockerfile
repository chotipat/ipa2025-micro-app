FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pytest.ini.test pytest.ini
COPY worker/ worker/
COPY api_service/ api_service/
COPY test/ test/

ENV PYTHONPATH=/app

CMD ["pytest", "-v"]
