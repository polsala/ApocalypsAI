# nightly-docker-quote-server

A tiny Dockerized Go HTTP server that returns a random whimsical quote on each request.

## Build

```sh
docker build -t nightly-docker-quote-server .
```

## Run

```sh
docker run -p 8080:8080 nightly-docker-quote-server
```

Visit http://localhost:8080/ to see a random quote.

## How it works

The server holds an in‑memory slice of quotes and picks one with math/rand on each request.

## Testing

```sh
go test ./...
```
