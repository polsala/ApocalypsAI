# nightly-docker-quote-of-the-day

A whimsical Dockerized HTTP service that serves a random inspirational quote each time you hit `/quote`. Perfect for adding a splash of positivity to your dev environment.

## Usage

```sh
docker build -t quote-of-the-day .
docker run -p 8080:8080 quote-of-the-day
```

Then request a quote:

```sh
curl http://localhost:8080/quote
```

Typical response:

```json
{"quote":"Your chosen quote here."}
```

## Implementation

The service is a tiny Flask app that selects a random line from `quotes.txt`. The Dockerfile builds a lightweight Python image.

## Testing

Run the tests inside the repository (no network required):

```sh
docker run --rm -v $(pwd):/app -w /app python:3.11-slim bash -c "pip install -r requirements.txt && pytest"
```
