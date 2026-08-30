FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src/
COPY README.md ./
ENTRYPOINT ["python", "-m", "src.size_estimator"]
