# nightly-echo-void

**A whimsical concurrent UDP echo server and client for measuring round‑trip latency.**

## Overview
`nightly-echo-void` spins up a tiny UDP "void" that echoes back any message you send, prefixing it with a nanosecond timestamp.  A companion client can fire multiple messages concurrently and report the round‑trip time for each.  Perfect for quick network diagnostics—or just for fun in a post‑apocalyptic bunker.

## Build & Run
```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-echo-void

# Build the binary (optional)
go build -o echo-void ./src/main.go
```

## Server Mode
```bash
# Run the UDP echo server on port 9000 (default)
go run ./src/main.go -mode server -port 9000
```
The server will listen on `0.0.0.0:9000` and echo back any incoming packet with a timestamp.

## Client Mode
```bash
# Send 5 messages to the server at localhost:9000
go run ./src/main.go -mode client -address localhost:9000 -count 5 -message "Hello Void"
```
Flags:
- `-mode`   : `server` or `client` (required)
- `-port`   : UDP port for the server (default `9000`)
- `-address`: `<host>:<port>` of the server (client only)
- `-count`  : Number of messages to send (client only, default `1`)
- `-message`: Payload string to send (client only, default `ping`)

## How It Works
* **Server** – Listens on a UDP socket. For each packet it receives, it captures `time.Now().UnixNano()`, formats `"<timestamp>:<payload>"`, and sends that back to the sender.
* **Client** – Sends the configured payload, waits for the echoed response, parses the timestamp, and prints the round‑trip latency in milliseconds.

## Testing
Run the deterministic unit tests with:
```bash
go test ./tests
```
The test suite starts an in‑process server, pings it, and verifies that the echoed payload matches the original message.

## License
MIT © ApocalypsAI
