# nightly-docker-quote-server

A whimsical Dockerized Flask service that returns a random inspirational quote at `/quote`. Useful for testing HTTP clients or adding a splash of positivity to CI pipelines.

## Build

```sh
docker build -t nightly-docker-quote-server .
```

## Run

```sh
docker run -p 5000:5000 nightly-docker-quote-server
```

## Endpoint

`GET http://localhost:5000/quote` returns JSON:

```json
{"quote":"..."}
```

## Tests

Run `pytest -q` inside the repository (no Docker needed).
