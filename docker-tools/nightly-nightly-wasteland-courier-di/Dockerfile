FROM python:3.9-slim-buster

WORKDIR /app

COPY src/requirements.txt .
COPY src/app.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
