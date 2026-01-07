# Nightly Concurrent Ping Sweeper

## Overview
A whimsical yet useful Go utility that concurrently checks the reachability of multiple `host:port` endpoints using TCP connections and reports latency statistics in JSON.

## Features
- Reads targets from command‑line arguments or **stdin** (one per line)
- Performs checks concurrently (default 10 workers)
- Outputs a JSON array with fields: `host`, `reachable`, `latency_ms`
- Zero external dependencies; pure Go standard library

## Installation
```sh
go build -o ping-sweeper ./src/main.go
```

## Usage
```sh
# From a file
cat hosts.txt | ./ping-sweeper

# Direct arguments
./ping-sweeper example.com:80 localhost:22
```

## Example output
```json
[
  {"host":"example.com:80","reachable":true,"latency_ms":23},
  {"host":"localhost:22","reachable":true,"latency_ms":1},
  {"host":"nonexistent:1234","reachable":false,"latency_ms":0}
]
```

## License
MIT
