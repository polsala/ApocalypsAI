# nightly-echo-lag-aggregator

A whimsical concurrent latency aggregator. It pings multiple hosts (via TCP handshake) in parallel and prints an ASCII bar chart representing round‑trip times.

## Usage

```sh
go run ./src/main.go example.com google.com github.com
```

Output:

```
example.com  23ms  ███
google.com   45ms  ██████
github.com   78ms  █████████
```

The bar length is proportional to latency (1 block per 10 ms, rounded).

## How it works

- Each host is dialed on port 80 concurrently.
- Latency is measured from start to successful connection.
- Results are sorted by latency and displayed.

## Testing

Run `go test ./...` to execute the deterministic unit tests.
