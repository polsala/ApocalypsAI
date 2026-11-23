# Nightly Docker Quote Server

A whimsical Dockerized HTTP server that returns a random apocalypse‑themed quote on each request.

## Usage

```sh
docker build -t nightly-quote-server .

docker run -p 8080:8080 nightly-quote-server
```

Then visit `http://localhost:8080/` to receive a JSON payload:

```json
{"quote":"..."}
```

## How it works

The server is written in Go, compiled inside the Docker image, and serves on port 8080.

## Extending

Add more quotes to `src/main.go` (the `quotes` slice) and rebuild the image.
