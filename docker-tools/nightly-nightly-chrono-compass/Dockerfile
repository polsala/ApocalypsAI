FROM python:3.9-slim-buster

WORKDIR /app

# Install build dependencies for ntplib and other potential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/chrono_compass.py .

CMD ["python", "chrono_compass.py"]
