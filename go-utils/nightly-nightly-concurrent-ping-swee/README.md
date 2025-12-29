# nightly-concurrent-ping-sweeper

A tiny Go utility that pings a list of hosts concurrently and prints the average round‑trip time. Useful for quick network health checks in a post‑apocalyptic bunker.

## Usage

```sh
go run ./src/main.go host1.com host2.com host3.com
```

If no hosts are supplied, the program reads newline‑separated hosts from STDIN.

## How it works

- Each host is pinged in its own goroutine.
- Results are sent over a channel.
- After all pings finish, the average latency is calculated and printed.

## Testing

Run `go test ./...` to execute the deterministic unit tests that mock network latency.
