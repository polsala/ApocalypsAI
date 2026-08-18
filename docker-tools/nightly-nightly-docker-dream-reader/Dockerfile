FROM python:3.9-slim-buster

WORKDIR /app

COPY src/ /app/src/

RUN chmod +x /app/src/entrypoint.sh

ENTRYPOINT ["/app/src/entrypoint.sh"]
