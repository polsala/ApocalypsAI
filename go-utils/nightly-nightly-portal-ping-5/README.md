# nightly-portal-ping

**nightly-portal-ping** is a tiny Go utility that pings a list of TCP hosts concurrently and reports the round‑trip latency for each. It is useful for quickly checking the reachability and responsiveness of services without leaving the terminal.

## Features

- Accepts any number of `host:port` arguments.
- Performs all pings in parallel using Go goroutines.
- Configurable timeout (default 2 seconds).
- Human‑readable output sorted by latency.
- Zero external dependencies – just the Go standard library.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-portal-ping
go build -o portal-ping ./src/main.go
```

## Usage

```bash
./portal-ping -timeout=3s example.com:80 8.8.8.8:53 localhost:22
```

The program will print something like:

```
example.com:80   23.4ms
8.8.8.8:53       31.1ms
localhost:22     timeout
```

## Testing

Run the unit tests with:

```bash
go test ./tests
```

The tests use a mock pinger to ensure deterministic, offline execution.

## License

MIT © ApocalypsAI community
