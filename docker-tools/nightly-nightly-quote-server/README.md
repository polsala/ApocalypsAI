# nightly-quote-server

A whimsical Dockerized HTTP server that serves a random quote on each request.

## Overview

The server runs a tiny Flask app inside a Docker container. When you `GET /` it returns a JSON payload with a random quote selected from a curated list.

## Build

```sh
docker build -t nightly-quote-server .
```

## Run

```sh
docker run -p 8080:8080 nightly-quote-server
```

Then visit `http://localhost:8080/` to see a quote.

## Extending

Add more quotes to `src/app.py` (the `QUOTES` list).
