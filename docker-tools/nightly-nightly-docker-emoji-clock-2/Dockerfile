FROM python:3.11-slim
WORKDIR /app
COPY src/clock.py /app/clock.py
RUN chmod +x /app/clock.py
ENTRYPOINT ["python", "/app/clock.py"]
