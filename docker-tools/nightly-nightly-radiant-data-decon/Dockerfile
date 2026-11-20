FROM python:3.9-slim-buster

WORKDIR /app

COPY src/decontaminator.py .

CMD ["python", "decontaminator.py", "/app/input", "/app/output"]
