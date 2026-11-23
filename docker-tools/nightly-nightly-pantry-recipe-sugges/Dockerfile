FROM python:3.11-slim

WORKDIR /app

COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "app.py"]
