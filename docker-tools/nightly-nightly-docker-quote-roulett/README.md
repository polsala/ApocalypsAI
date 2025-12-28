# nightly-docker-quote-roulette

A whimsical Docker container that prints a random inspirational quote each time it starts. Perfect for adding a splash of motivation to your CI pipelines or local dev sessions.

## Usage

```sh
docker run --rm ghcr.io/your-org/nightly-docker-quote-roulette
```

You can also specify a deterministic quote for testing:

```sh
docker run --rm -e QUOTE_INDEX=0 ghcr.io/your-org/nightly-docker-quote-roulette
```

## How it works

The container runs a tiny Python script that reads a bundled list of quotes and prints one. If the environment variable `QUOTE_INDEX` is set, the script will print the quote at that index (zero‑based), making the output predictable for tests.

## Dockerfile

```Dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY src/ /app/
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "app.py"]
```
