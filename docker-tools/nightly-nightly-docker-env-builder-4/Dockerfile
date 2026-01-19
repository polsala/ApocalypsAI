# Dockerfile for Nightly Docker Env Builder

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py .

CMD ["python", "main.py"]
