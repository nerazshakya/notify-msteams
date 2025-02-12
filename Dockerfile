FROM python:3.9-slim

WORKDIR /app

COPY main.py notify.py /app/

RUN pip install requests

CMD ["python", "notify.py"]