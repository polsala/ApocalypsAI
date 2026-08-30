FROM python:3.9-slim-buster

WORKDIR /app

# Install Docker SDK for Python
RUN pip install docker

COPY src/dust_bunny_sweeper.py .
COPY src/entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
