# Quote Mixer Docker Service

## Overview
A lightweight Docker container that runs a Go HTTP server. When you `GET /quote`, it returns a JSON object with a randomly mixed quote combining a post‑apocalyptic line and an inspirational saying.

## Usage
```sh
docker build -t quote-mixer .
docker run -p 8080:8080 quote-mixer
```
Then request:
```sh
curl http://localhost:8080/quote
# {"quote":"..."}
```

## Implementation
- Go 1.22, standard library only.
- Docker multi‑stage build for a small image (~5 MB).

## Testing
```sh
go test ./...
```
