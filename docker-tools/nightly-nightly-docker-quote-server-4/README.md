# Nightly Docker Quote Server

A whimsical Dockerized Go HTTP server that returns a random quote each time you hit the root endpoint.

## Build

```sh
docker build -t nightly-docker-quote-server .
```

## Run

```sh
docker run -p 8080:8080 nightly-docker-quote-server
```

## Usage

```sh
curl http://localhost:8080/
```

Will return a plain‑text quote, e.g.:

> "The early bird gets the worm, but the second mouse gets the cheese."

## How it works

The server is a single‑binary Go program compiled inside a multi‑stage Docker build. On each request it picks a random entry from an embedded slice of whimsical quotes.

## Testing

```sh
go test ./...
```
