FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py .
COPY src/blueprints blueprints/
COPY src/manifests manifests/

ENTRYPOINT ["python"]
CMD ["app.py", "--help"]
