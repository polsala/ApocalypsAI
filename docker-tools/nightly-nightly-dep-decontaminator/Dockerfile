FROM python:3.9-slim-buster

WORKDIR /app

COPY src/decontaminator.py .
COPY src/config.json .

ENTRYPOINT ["python", "decontaminator.py"]
