# Nightly Apocalypse Echo

## Overview

A tiny Go utility that runs an HTTP server. Clients send a message via the `/echo` endpoint and receive a JSON payload containing the original message and a randomly chosen post‑apocalyptic phrase. The server handles requests concurrently using Go's built‑in HTTP server.

## Build & Run

```sh
go build -o apocalypse-echo ./src
./apocalypse-echo
```

The server listens on port 8080 (or `$PORT` env var).

## Usage

```sh
curl "http://localhost:8080/echo?msg=Hello%20World"
```

Response:

```json
{
  "original": "Hello World",
  "doom": "The sky cracks like shattered glass"
}
```

## Testing

```sh
go test ./...
```
