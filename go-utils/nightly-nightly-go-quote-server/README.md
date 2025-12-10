# nightly-go-quote-server

A lightweight Go utility that runs an HTTP server exposing a single endpoint `/quote`. Each request returns a random whimsical quote in JSON format. The server is fully concurrent (handled by Go's net/http) and can be seeded via a query parameter for deterministic responses, which is handy for testing.

## Features
- Zero external dependencies – only the Go standard library.
- Concurrent request handling out‑of‑the‑box.
- Optional `seed` query parameter to produce repeatable results.
- Simple Dockerfile for containerised deployment (optional).

## Usage
```bash
# Build and run locally
go run src/main.go
```
The server listens on `localhost:8080` by default.

### Endpoints
- `GET /quote` – Returns a random quote.
- `GET /quote?seed=123` – Returns a deterministic quote based on the supplied seed (useful for testing).

#### Example response
```json
{ "quote": "The early bird gets the worm, but the second mouse gets the cheese." }
```

## Testing
```bash
go test ./tests
```
All tests run offline and use the deterministic seed mode.

## Docker (optional)
```Dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/ ./src/
RUN go build -o /quote-server src/main.go

FROM alpine:latest
COPY --from=builder /quote-server /quote-server
EXPOSE 8080
ENTRYPOINT ["/quote-server"]
```
Build and run:
```bash
docker build -t quote-server .
docker run -p 8080:8080 quote-server
```
