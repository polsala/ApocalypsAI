# nightly-go-ping-pong

**A concurrent, whimsical ping utility written in Go**

## Overview
`nightly-go-ping-pong` pings a list of hosts concurrently and rates each host's latency with a fun animal metaphor:

- 🐇 **Lightning rabbit** – < 50 ms
- 🐦 **Swift sparrow** – 50‑149 ms
- 🐢 **Steady turtle** – 150‑299 ms
- 🐌 **Slothful snail** – ≥ 300 ms

The tool is deliberately light‑hearted while still being useful for quick network checks.

## Build
```bash
go build -o pingpong ./src/main.go
```

## Usage
```bash
./pingpong example.com google.com 8.8.8.8
```
Output example:
```
example.com: 🐦 Swift sparrow (87 ms)
google.com: 🐇 Lightning rabbit (23 ms)
8.8.8.8: 🐢 Steady turtle (172 ms)
```
If a host cannot be reached, an error indicator is shown.

## Testing
```bash
go test ./tests
```
The tests use a mock ping function, so they run offline and deterministically.
