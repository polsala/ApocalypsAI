# Portal Ping‑Pong

A tiny Go utility that can act as a UDP “ping‑pong” server or client. The server echoes any incoming packet back to the sender, handling each request concurrently. The client sends a single message and reports the round‑trip time, useful for quick network latency checks in a post‑apocalyptic bunker.

## Build & Run

```sh
go run src/main.go -mode=server -port=9000   # start server
go run src/main.go -mode=client -addr=localhost:9000 -msg="Hello, wasteland!"   # run client
```

## Flags

- `-mode` – `server` or `client` (required)
- `-port` – UDP port for the server (default 9000)
- `-addr` – address of the server for the client (e.g., `localhost:9000`)
- `-msg` – message to send (client only, default “ping”)

## Testing

```sh
go test ./...
```
