FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pytest.ini.test pytest.ini
COPY .env.test .env.test
COPY worker/ worker/
COPY api_service/ api_service/
COPY test/ test/

RUN mv test/entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

CMD ["pytest", "-v"]
