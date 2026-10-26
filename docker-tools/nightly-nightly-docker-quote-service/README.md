# nightly-docker-quote-service

A whimsical Dockerized HTTP service that serves a daily post‑apocalyptic quote. Each request to `/quote` returns a JSON object with a quote selected deterministically from a short list based on the current UTC date, so the same day always yields the same quote. Perfect for adding a touch of drama to CI logs or local terminals.

## Build

```sh
docker build -t nightly-docker-quote-service .
```

## Run

```sh
docker run -p 8080:8080 nightly-docker-quote-service
```

Then query:

```sh
curl http://localhost:8080/quote
```

Example output:

```json
{"quote":"The ashes whisper, \"Tomorrow is a myth.\""}
```

## How it works

The container runs a tiny Python 3.11 HTTP server (`src/app.py`). The server calculates the day‑of‑year and picks a quote from a hard‑coded list, guaranteeing deterministic output without external APIs.

## Tests

Run the unit tests locally (no Docker needed):

```sh
python -m unittest discover -s tests
```
