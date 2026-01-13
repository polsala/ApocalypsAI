FROM python:3.11-slim
WORKDIR /app
COPY src/main.py src/main.py
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "src/main.py", "--serve"]

