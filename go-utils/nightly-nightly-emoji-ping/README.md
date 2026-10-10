# Nightly Emoji Ping

A whimsical concurrent ping utility written in Go. It pings multiple hosts in parallel and reports their status with fun emojis that reflect latency.

## Features

- Concurrent ping of any number of hosts
- Timeout handling
- Emoji feedback:
  - `🚀` ultra‑fast (< 50 ms)
  - `⚡` fast (50‑150 ms)
  - `🐢` slow (> 150 ms)
  - `❌` unreachable
- Zero external dependencies (standard library only)

## Installation

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-ping
go build -o emoji-ping ./src/main.go
```

## Usage

```bash
./emoji-ping example.com google.com 192.0.2.1
```

Sample output:

```
example.com: up (23ms) 🚀
google.com: up (78ms) ⚡
192.0.2.1: down ❌
```

## Testing

```bash
go test ./tests
```

The test suite uses mocked ping functions, so it runs offline and deterministically.
