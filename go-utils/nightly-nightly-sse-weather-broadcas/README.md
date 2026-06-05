# nightly-sse-weather-broadcast

Utility that starts an HTTP server emitting whimsical weather updates via Server‑Sent Events (SSE). Useful for testing SSE clients or adding a bit of post‑apocalyptic flair to demos.

## Usage

```sh
go run src/main.go
```

The server listens on `http://localhost:8080/weather`. Connect with an SSE‑compatible client to receive events like:

```
event: weather
data: Acid rain, 42°C
```

## Options

- `-port` (default 8080) – port to listen on.
- `-interval` (default 2s) – time between events.

## Testing

Run `go test ./...` to execute the deterministic test suite.
