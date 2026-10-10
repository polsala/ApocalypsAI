FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/temporal_tidy.py .
ENTRYPOINT ["python", "temporal_tidy.py"]
