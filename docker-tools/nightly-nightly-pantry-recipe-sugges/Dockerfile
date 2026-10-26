FROM python:3.11-slim
WORKDIR /app
COPY src/app.py /app/app.py
# No external dependencies; stdlib only
ENTRYPOINT ["python", "app.py"]
