# nightly-concurrent-ping

A whimsical Go utility that concurrently pings multiple hosts and reports latency statistics.

## Overview

`nightly-concurrent-ping` accepts a list of hostnames or IP addresses, pings each of them in parallel, and prints the round‑trip time in milliseconds. It’s useful for quick network health checks in a post‑apocalyptic bunker.

## Build & Run

```sh
go build -o nightly-concurrent-ping ./src
./nightly-concurrent-ping example.com 8.8.8.8
```

## Output

```
example.com: 23ms
8.8.8.8: 12ms
```

## Testing

```sh
go test ./tests
```
