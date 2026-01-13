FROM python:3.11-slim
WORKDIR /app
COPY src/ .
RUN pip install --no-cache-dir requests
ENTRYPOINT ["python", "main.py"]
