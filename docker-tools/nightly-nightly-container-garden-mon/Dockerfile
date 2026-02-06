FROM python:3.9-slim-buster
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/garden_monitor.py .
CMD ["python", "garden_monitor.py"]
