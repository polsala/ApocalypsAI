FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install --no-cache-dir docker

COPY src/app.py .

ENV CONTAINER_NAMES=""
ENV POLLING_INTERVAL_SECONDS=60

CMD ["python", "app.py"]
