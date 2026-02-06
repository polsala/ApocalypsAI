# Nightly Ping Aggregator

A whimsical concurrent ping utility that measures latency to multiple hosts in parallel. Perfect for quick network health checks in a post‑apocalyptic setting.

## Build

```sh
go build -o ping-aggregator ./src
```

## Usage

```sh
./ping-aggregator host1:80 host2:443 ...
```

The tool will attempt a TCP connection to each address with a 2‑second timeout and print the measured latency or report the host as unreachable.
