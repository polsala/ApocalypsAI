FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install docker

COPY aura_reader.py .

CMD ["python", "aura_reader.py"]
