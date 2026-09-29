# nightly-concurrent-ping-sweeper

Concurrently pings a list of hosts (TCP connect to port 80) and reports latency statistics.

## Usage

```sh
go run ./src/main.go example.com google.com
```

Typical output:

```
example.com: 23ms
google.com: 12ms
--- Summary ---
Successful: 2, Failed: 0, Average latency: 17.5ms
```

## How it works

- Spawns a goroutine per host.
- Uses a 2‑second timeout for each connection.
- Collects results via channels.
- Prints per‑host latency and a summary.

## Testing

`go test ./...` runs deterministic unit tests that mock network calls.
