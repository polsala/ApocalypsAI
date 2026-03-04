# Nightly Radiation Broadcast

A tiny Go service that pretends to collect radiation levels from a post‑apocalyptic sensor network and exposes the current level on an HTTP endpoint.

## Features

- Concurrent HTTP server listening on `:8080`
- Pluggable `Sensor` interface (real implementation returns a placeholder, tests inject a mock)
- JSON response: `{ "level": <int> }`
- Zero external dependencies – just the Go standard library

## Build

```bash
go build -o radiation-broadcast ./src
```

## Run

```bash
./radiation-broadcast
```

The server will start and listen on port 8080. Access the current radiation level:

```bash
curl http://localhost:8080/radiation
```

## Testing

```bash
go test ./tests
```

The test suite injects a mock sensor to verify deterministic output.
