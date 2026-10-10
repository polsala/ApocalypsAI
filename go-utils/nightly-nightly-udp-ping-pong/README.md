# nightly-udp-ping-pong

A tiny Go utility that can act as a **UDP ping‑pong server** or **client**.  The server simply echoes back any message it receives, prefixing it with `Pong:`.  The client sends a configurable number of ping messages, measures round‑trip latency, and prints a short report.

## Why?
- Quick way to check UDP reachability between two hosts.
- Fun demonstration of Go's concurrency primitives.
- No external dependencies – just the Go standard library.

## Build
```bash
# From the repository root
cd utils/nightly-udp-ping-pong
go build -o udp-ping-pong ./src/main.go
```

## Usage
### Server
```bash
./udp-ping-pong -mode=server -listen=:9000
```
- `-listen` defaults to `:9000`.
- Handles each incoming packet in its own goroutine, so it can serve many clients concurrently.

### Client
```bash
./udp-ping-pong -mode=client -target=localhost:9000 -count=10 -interval=500ms
```
- `-target` is the server address.
- `-count` is how many pings to send (default 5).
- `-interval` is the pause between pings (default 1s).

The client prints each ping/​pong pair with its latency and a final summary (min/​max/​avg).

## License
MIT © ApocalypsAI
