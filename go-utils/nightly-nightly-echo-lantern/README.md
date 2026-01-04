# Nightly Echo Lantern

A whimsical HTTP echo server that adds a lantern emoji to every response. Useful for debugging HTTP clients and visualizing request payloads.

## Usage

```bash
go run src/main.go
```

The server listens on `localhost:8080`. Send a request:

```bash
curl -X POST http://localhost:8080/echo -d '{"msg":"hello"}' -H "Content-Type: application/json"
```

Response:

```json
{
  "echo": "{\"msg\":\"hello\"}",
  "lantern": "🏮"
}
```

## Testing

Run tests with:

```bash
go test ./...
```
