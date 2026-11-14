# nightly-ping-pong

## Summary
A whimsical concurrent network ping utility that measures latency to multiple hosts and reports the results with playful commentary.

## Usage
```sh
go run src/main.go host1:port host2:port ...
```
Example:
```sh
go run src/main.go google.com:80 github.com:443
```
Output:
```
google.com:80 → 23ms 🚀
github.com:443 → 45ms 🌟
Average latency: 34ms 🎉
```

## How it works
- Accepts a list of `host:port` arguments.
- Launches a goroutine per target.
- Uses TCP connect with a 2‑second timeout to approximate latency.
- Collects results and prints each latency plus an emoji based on speed.
- If a host is unreachable, reports "timeout".

## Testing
Run `go test ./...` to execute deterministic unit tests that mock network calls.
