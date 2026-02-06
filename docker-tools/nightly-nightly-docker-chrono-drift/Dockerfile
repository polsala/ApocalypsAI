FROM python:3.9-slim-buster

WORKDIR /app

COPY src/chrono_drift.py /app/chrono_drift.py
COPY src/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
