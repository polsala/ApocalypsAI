# nightly-quote-server

A tiny Dockerized Flask service that serves a random quote of the day from a built‑in list. Useful for testing HTTP clients or as a whimsical placeholder service.

## Build

```sh
docker build -t nightly-quote-server .
```

## Run

```sh
docker run -p 8080:8080 nightly-quote-server
```

## Endpoint

`GET /quote` returns JSON:

```json
{ "quote": "...", "author": "..." }
```

## Tests

Run the unit tests (no Docker needed):

```sh
python -m unittest discover -s tests
```
