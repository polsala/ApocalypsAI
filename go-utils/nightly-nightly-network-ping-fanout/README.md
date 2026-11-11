# Nightly Network Ping Fanout

A whimsical yet practical Go utility that concurrently attempts TCP connections to a list of hosts (e.g., radio beacons, supply caches) and reports which are reachable along with latency. Perfect for scavengers mapping the broken internet.

## Usage

```sh
go run ./src/main.go host1:port host2:port ...
```

Example:

```sh
go run ./src/main.go example.com:80 10.0.0.1:22
```

The program prints a line per host indicating success or failure.

## How it works

- Accepts `host:port` arguments.
- Launches a goroutine per address.
- Uses a 2‑second timeout for each TCP dial.
- Collects results and prints a concise report.

## Testing

Run `go test ./...` to execute deterministic unit tests that mock network calls.
