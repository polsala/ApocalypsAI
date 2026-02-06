FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV FLASK_APP=src/app.py
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
