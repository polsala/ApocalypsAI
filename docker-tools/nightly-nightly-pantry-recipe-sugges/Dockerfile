FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "src.main"]
