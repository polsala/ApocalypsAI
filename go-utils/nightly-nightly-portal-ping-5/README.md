# nightly-portal-ping

A whimsical concurrent ping utility that checks if the apocalypse has reached your favorite hosts. It pings multiple hosts in parallel using TCP handshakes and reports min/avg/max latency.

## Build

```sh
go build -o portal-ping ./src
```

## Usage

```sh
./portal-ping host1.com host2.com 8.8.8.8
```

The program will attempt to connect to each host on port 80 with a 2‑second timeout and display latency statistics.

## How it works

- Uses goroutines to ping hosts concurrently.
- Measures time to establish a TCP connection.
- Reports per‑host latency and overall min/avg/max.

## Testing

Run `go test ./...` to execute deterministic unit tests that mock network latency.
