# nightly-portal-ping

A tiny Go utility that concurrently attempts a TCP connection to port 80 of each supplied host, measures the round‑trip latency, and prints a JSON array of results.

## Why?
In the post‑apocalyptic wasteland of network diagnostics, you need a fast, whimsical way to see which outposts are still online. `portal-ping` does exactly that, leveraging Go's goroutine magic for speed.

## Installation
```bash
# Clone the repository (or copy the generated folder)
git clone https://github.com/your-org/ApocalypsAI.git
cd go-utils/nightly-portal-ping
# Build the binary
go build -o portal-ping ./src/main.go
```

## Usage
```bash
./portal-ping example.com 8.8.8.8 localhost
```
You can also adjust the timeout (default 2s):
```bash
./portal-ping -timeout=1s example.com
```
The output is a pretty‑printed JSON array, e.g.:
```json
[
  {
    "host": "example.com",
    "reachable": true,
    "latency_ms": 23.4
  },
  {
    "host": "8.8.8.8",
    "reachable": true,
    "latency_ms": 12.7
  },
  {
    "host": "nonexistent.local",
    "reachable": false,
    "error": "dial tcp: lookup nonexistent.local: no such host"
  }
]
```

## Testing
```bash
go test ./tests
```
The test suite mocks network calls, so it runs offline and deterministically.
