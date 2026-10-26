FROM python:3.9-slim-buster

LABEL maintainer="ApocalypsAI Nightly Integrator"

WORKDIR /app

COPY src/dust_bunny_sweeper.py /app/
COPY src/entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
