# Nightly Apocalypse Beacon

**Nightly Apocalypse Beacon** is a whimsical yet practical Go utility that concurrently pings a list of TCP hosts and reports their reachability with apocalypse‑themed emojis.

## Features

- Fully concurrent – each host is pinged in its own goroutine.
- Pluggable `PingProvider` interface makes the core logic testable without real network calls.
- Simple command‑line interface: just pass `host:port` arguments.
- No external dependencies beyond the Go standard library.

## Installation

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-apocalypse-beacon/src
go build -o beacon .
```

## Usage

```bash
./beacon example.com:80 192.0.2.1:22 badhost:1234
```

Typical output:

```
✅ example.com:80 responded in 23ms
✅ 192.0.2.1:22 responded in 45ms
☠️ badhost:1234 is unreachable (dial tcp: lookup badhost: no such host)
```

## Testing

The utility includes a deterministic test suite that uses a mock `PingProvider` to avoid real network traffic.

```bash
go test ./...
```

## License

MIT © ApocalypsAI community
