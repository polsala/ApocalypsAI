# nightly-portal-ping-multiplexer

A whimsical concurrent TCP ping utility that opens a portal to check the latency of multiple hosts at once.

## Overview

`portal-ping` reads a list of hostnames (or IPs) and pings each of them concurrently using TCP connections. It reports the round‑trip time or reports a timeout/failure. Perfect for quick network health checks in a post‑apocalyptic setting.

## Installation

```sh
go build -o portal-ping ./src/main.go
```

## Usage

```sh
./portal-ping host1.example.com host2.example.com 8.8.8.8
```

Output:

```
host1.example.com: 23ms
host2.example.com: timeout
8.8.8.8: 12ms
```

## Testing

```sh
go test ./tests
```

## Design

- Uses goroutines and a channel to perform pings concurrently.
- `PingFunc` is injectable for deterministic unit tests.
