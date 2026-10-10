# nightly-portal-ping

**nightly-portal-ping** is a tiny Go utility that pings a list of TCP hosts concurrently and reports the round‑trip latency for each.  It’s useful for quick health‑checks, network diagnostics, or just for fun when you want to see how fast your favorite services respond.

## Features

- Concurrent probing of any number of `host:port` endpoints.
- Configurable timeout per probe.
- Returns latency as a `time.Duration` (or `-1` for unreachable hosts).
- Zero external dependencies – just the Go standard library.

## Build & Run

```bash
# Clone the repository (or copy the generated folder) and cd into it
cd utils/nightly-portal-ping

# Build the binary
go build -o portal-ping ./src/main.go

# Run with a list of hosts (example)
./portal-ping localhost:80 example.com:80
```

The binary will print something like:

```
localhost:80: 1.23ms
example.com:80: 45.6ms
```

If a host is unreachable, it prints `unreachable`.

## Testing

Run the unit tests with:

```bash
go test ./tests/...
```

The tests spin up mock TCP listeners locally, so they are deterministic and require no network access.

## License

MIT © ApocalypsAI
