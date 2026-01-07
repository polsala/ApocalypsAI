# Portal Ping

A whimsical concurrent ping utility that "opens portals" to a list of hosts and measures round‑trip latency. Useful for quick health checks of multiple services.

## Installation

```sh
go build -o portal-ping ./src/main.go
```

## Usage

```sh
./portal-ping host1.example.com host2.example.com
```

The program prints a JSON array where each element contains:

- `host`: the target hostname
- `latency_ms`: measured latency in milliseconds (omitted on error)
- `error`: error message if the ping failed (omitted on success)

Example output:

```json
[
  {"host":"example.com","latency_ms":42},
  {"host":"unreachable.local","error":"dial timeout"}
]
```

## How it works

- Uses Go's concurrency (goroutines + a worker pool) to ping up to **10** hosts in parallel.
- Measures latency by establishing a TCP connection to port **80** and timing the round‑trip.
- Results are marshaled to JSON for easy consumption by scripts or CI pipelines.

## Testing

```sh
go test ./tests
```

The test suite uses a mock ping function so it runs deterministically offline.
