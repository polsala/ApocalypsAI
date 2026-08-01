# Nightly Apocalypse Tip Server

A whimsical yet useful utility that runs inside a Docker container and serves random post‑apocalyptic survival tips over HTTP.

## Features
- Small footprint (multi‑stage Alpine build)
- Deterministic tip selection for testing (optional `seed` query param)
- JSON response: `{ "tip": "..." }`
- No external dependencies at runtime

## Build the Docker image
```bash
docker build -t apocalypse-tip-server .
```

## Run the container
```bash
docker run -p 8080:8080 apocalypse-tip-server
```
The server will listen on port **8080**. Access a tip with:
```bash
curl http://localhost:8080/tip
```
You can also provide a deterministic seed (useful for reproducible results):
```bash
curl "http://localhost:8080/tip?seed=42"
```

## Development
The Go source lives in `src/main.go`. Unit tests are in `tests/main_test.go` and can be run with:
```bash
go test ./...
```

## License
MIT © ApocalypsAI
