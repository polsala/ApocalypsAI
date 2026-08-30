# nightly-go-quote-server

A whimsical yet useful concurrent HTTP server written in Go that serves random quotes.

## Features
- Serves a random quote at `/quote` (JSON: {"quote":"..."}).
- Health check endpoint at `/health` returning `OK`.
- Thread‑safe concurrent access using a mutex.
- Zero external dependencies; just the Go standard library.

## Build & Run
```sh
go build -o quote-server ./src
./quote-server
```
The server listens on `localhost:8080`.

## Endpoints
- `GET /quote` – returns a random quote.
- `GET /health` – returns plain text `OK`.

## Testing
```sh
go test ./tests
```
