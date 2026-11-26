# nightly-quote-server

A whimsical yet practical Go utility that runs a lightweight HTTP server exposing a single endpoint:

```
GET /quote
```

The endpoint returns a JSON payload with a random quote and its author. The server caches the last quote for a configurable TTL (default 5 seconds) to reduce churn while still providing variety.

## Features

- **Concurrent**: Handles many simultaneous requests using Go's built‑in HTTP server.
- **Cache**: Simple in‑memory cache with configurable TTL.
- **Deterministic tests**: Uses a fixed random seed in the test suite.
- **Zero external dependencies** – only the Go standard library.

## Build & Run

```bash
# Clone the repository (or copy the generated files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-quote-server

# Build the binary
go build -o quote-server ./src/main.go

# Run the server (listens on port 8080)
./quote-server
```

The server will log a startup message and begin serving requests on `http://localhost:8080/quote`.

## Example Request

```bash
curl http://localhost:8080/quote
```

Possible response:

```json
{ "text": "When the world ends, at least we have coffee.", "author": "Anonymous" }
```

## Testing

```bash
go test ./tests
```

The test suite starts the handler with a deterministic random seed and verifies the JSON output.
