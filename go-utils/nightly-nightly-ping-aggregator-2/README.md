# nightly-ping-aggregator

A whimsical concurrent ping aggregator for the post‑apocalypse. Given a list of hostnames, it pings them in parallel (via TCP handshake) and reports min/avg/max latency.

## Build

```sh
go build -o ping-aggregator ./src
```

## Usage

```sh
./ping-aggregator host1.com example.org 8.8.8.8
```

The program prints a JSON array of results, each containing the host, latency (in milliseconds) or an error message.

## Testing

```sh
go test ./...
```
