FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src/
RUN pip install --no-cache-dir Flask
EXPOSE 8080
CMD ["python", "-m", "src.app"]
