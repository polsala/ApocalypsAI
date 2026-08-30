# Apocalyptic Ping Oracle

A whimsical concurrent ping oracle that reports simulated latencies to multiple hosts.

## Overview

`nightly-apocalypse-ping-oracle` takes a list of hostnames or IP addresses and concurrently "pings" them, reporting a simulated latency in milliseconds. In real mode it measures actual TCP connection latency; in demo mode it uses a deterministic pseudo‑random generator so you can reproduce results.

## Build & Run

```sh
go build -o ping-oracle ./src
./ping-oracle example.com 8.8.8.8 localhost
```

## Testing

```sh
go test ./tests
```

## How it works

The tool spawns a goroutine per host, uses a `LatencyProvider` interface to obtain latency, and aggregates results. The default provider performs a TCP dial to port 80 with a timeout and measures elapsed time. A mock provider is used in tests for deterministic output.
