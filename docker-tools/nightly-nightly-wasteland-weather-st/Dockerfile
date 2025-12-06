FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py .
COPY tests/ tests/

ENV LOCATION="Chernobyl"
ENV API_KEY=""

CMD ["python", "app.py"]
