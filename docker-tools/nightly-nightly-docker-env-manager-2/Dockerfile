# Dockerfile for the DockerEnvManager

FROM python:3.10-slim

WORKDIR /app

COPY src/ /app/src/
COPY environments/ /app/environments/

RUN pip install --no-cache-dir PyYAML

CMD ["python", "src/main.py"]
