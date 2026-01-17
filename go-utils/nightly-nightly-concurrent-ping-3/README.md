# nightly-concurrent-ping

A whimsical Go utility that concurrently "pings" a list of hosts (or any strings) and reports simulated latency in milliseconds. Useful for quick sanity checks or as a teaching example of Go concurrency.

## Usage

```sh
go run src/main.go example.com google.com
```

Outputs:

```
example.com: 42ms
google.com: 13ms
```

## How it works

- Spawns a goroutine per host.
- Uses a timeout‑aware TCP dial to measure round‑trip time.
- Falls back to a mock latency provider when network access is unavailable.

## Testing

Run `go test ./...` to execute deterministic unit tests that mock the latency provider.
