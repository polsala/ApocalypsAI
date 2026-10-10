# Apocalyptic Ping Pong

A whimsical concurrent ping utility written in Go. It checks the latency of multiple hosts in parallel and prints a fun ASCII emoji representing the speed.

## Build

```sh
go build -o pingpong ./src
```

## Usage

```sh
./pingpong host1.com host2.com 8.8.8.8
```

Output example:

```
⚡ host1.com (23ms)
~ host2.com (120ms)
🐢 8.8.8.8 (350ms)
```

## How it works

- Uses goroutines to ping each host concurrently.
- Measures TCP connection latency to port 80.
- Maps latency to an emoji:
  - ⚡ < 50 ms (fast)
  - ~ 50‑200 ms (moderate)
  - 🐢 ≥ 200 ms (slow)

## Tests

Run `go test ./...` to execute deterministic unit tests that mock network latency.
