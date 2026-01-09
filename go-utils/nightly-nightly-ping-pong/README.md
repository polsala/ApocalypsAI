# nightly-ping-pong

A whimsical concurrent ping utility written in Go. It measures the round‑trip latency to a list of hosts (via TCP handshake) using goroutines and prints a fun summary.

## Build

```sh
go build -o nightly-ping-pong ./src
```

## Usage

```sh
./nightly-ping-pong host1.com host2.com ...
```

If no hosts are provided, it pings a default list of popular sites.

The tool reports each host's latency in milliseconds and a playful verdict (e.g., "Lightning fast", "Snail pace").

## Testing

```sh
go test ./tests
```
