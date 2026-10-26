# Portal Ping‑Pong

A whimsical concurrent network latency checker written in Go. It pings multiple hosts (via a quick TCP connection to port 80) in parallel and prints a report decorated with emojis indicating speed.

## Usage

```sh
go run ./src/main.go example.com google.com
```

or build:

```sh
go build -o portal-ping-pong ./src/main.go
./portal-ping-pong example.com google.com
```

## Output

```
🪐 Portal Ping‑Pong Report 🪐
example.com – 120ms (⚡)
google.com – 45ms (🚀)
nonexistent.tld – ❌ dial tcp: lookup nonexistent.tld: no such host
```

## Testing

```sh
go test ./tests/...
```

The tests mock the network calls, so they run offline.
