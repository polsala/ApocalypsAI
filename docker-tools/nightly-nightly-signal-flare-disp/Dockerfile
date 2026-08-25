FROM python:3.9-slim-buster

WORKDIR /app

COPY src/requirements.txt .
COPY src/app.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
