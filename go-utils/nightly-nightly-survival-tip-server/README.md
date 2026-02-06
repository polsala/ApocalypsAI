# nightly-survival-tip-server

A tiny Go HTTP server that serves a random post‑apocalyptic survival tip at `/tip`. Perfect for a quick morale boost in the wasteland.

## Usage

```sh
go run src/main.go
```

The server listens on `localhost:8080`. Retrieve a tip:

```sh
curl http://localhost:8080/tip
```

Example response:

```json
{"tip":"Always keep a spare water filter."}
```

## How it works

- A hard‑coded list of tips is embedded in the binary.
- Each request selects a tip at random using Go’s `math/rand`.
- The response is JSON with a single `tip` field.

## Testing

```sh
go test ./...
```
