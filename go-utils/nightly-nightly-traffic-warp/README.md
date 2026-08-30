# nightly-traffic-warp

A whimsical TCP proxy that adds configurable latency, jitter, and packet loss to simulate post‑apocalyptic network conditions.

## Installation

```sh
go build -o nightly-traffic-warp ./src
```

## Usage

```sh
./nightly-traffic-warp -listen :9000 -target example.com:80 -latency 100 -jitter 50 -loss 10
```

- `-listen` address to listen on.
- `-target` remote address to forward to.
- `-latency` base latency in milliseconds.
- `-jitter` max jitter in milliseconds (added/subtracted randomly).
- `-loss` packet loss percentage (0‑100).

## How it works

The proxy reads data from the client, optionally drops packets based on the loss rate, sleeps for the configured latency plus random jitter, then forwards the data to the target. The reverse direction is treated the same way.

## Testing

Run `go test ./...` to execute the deterministic unit tests.
