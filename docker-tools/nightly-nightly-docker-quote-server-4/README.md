# nightly-docker-quote-server

## Overview
A whimsical Docker container that runs a lightweight Flask web server. When you GET `/quote`, it returns a random post‑apocalyptic quote in JSON.

## Usage
```bash
docker build -t quote-server .

docker run -d -p 8080:8080 quote-server
curl http://localhost:8080/quote
```

## Deterministic testing
Set the environment variable `QUOTE_INDEX` to select a specific quote (0‑based). The test suite builds the image and runs the container with `QUOTE_INDEX=0` to verify output.

## Files
- `Dockerfile` – builds the image.
- `src/app.py` – Flask application.
- `requirements.txt` – Python dependencies.
- `tests/test_app.py` – unit tests.
