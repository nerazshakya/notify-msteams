FROM python:3.9-slim

WORKDIR /app

COPY notify.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/notify.py"]