# nightly-docker-quote-server

A whimsical Dockerized HTTP server that serves random quotes on demand.

## Overview

The server runs inside a Docker container and exposes an HTTP endpoint `/quote`. Each request returns a random quote from a curated list of whimsical sayings.

## Build

```sh
docker build -t nightly-docker-quote-server .
```

## Run

```sh
docker run -p 8080:8080 nightly-docker-quote-server
```

Visit `http://localhost:8080/quote` to receive a quote.

## Development

Run locally without Docker:

```sh
pip install Flask
python -m src.app
```

## Testing

```sh
python -m unittest discover -s tests
```
