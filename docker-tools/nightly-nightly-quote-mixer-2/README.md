# Nightly Quote Mixer

A whimsical Dockerized HTTP service that returns a randomly mixed inspirational and apocalyptic quote.

## Usage

```sh
# Build the Docker image
docker build -t nightly-quote-mixer .

# Run the container (exposes port 8080)
docker run -p 8080:8080 nightly-quote-mixer
```

The service will start and listen on port **8080**.

### Get a quote

```sh
curl http://localhost:8080/quote
# Example output: {\"quote\":\"Fortune favors the bold while the earth trembles.\"}
```

## How it works

The service maintains two hard‑coded lists – one of inspirational sayings and one of apocalyptic fragments. For each request it picks one entry from each list at random and concatenates them into a single sentence.

## Testing

The utility includes a Go test suite that can be run locally (requires Go 1.22 or later) or inside the container.

```sh
# Run tests locally
go test ./...
```

## Files

- `Dockerfile` – multi‑stage build for the Go binary
- `src/main.go` – HTTP server implementation
- `src/go.mod` – minimal Go module definition
- `tests/main_test.go` – deterministic unit tests using a fixed random seed

