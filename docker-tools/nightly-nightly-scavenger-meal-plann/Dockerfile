FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/
COPY tests/ ./tests/

# No external dependencies needed beyond the stdlib

ENTRYPOINT ["python", "-m", "src.app"]
