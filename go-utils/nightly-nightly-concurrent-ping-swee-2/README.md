# Nightly Concurrent Ping Sweeper

## Overview

`nightly-concurrent-ping-sweeper` is a lightweight Go commandâline utility that pings (via a TCP connect) a list of hosts concurrently and prints the latency results as JSON.  It is useful for quick network health checks, monitoring multiple services, or debugging connectivity issues without installing heavy tools.

## Features

- **Concurrent**: probes all hosts in parallel using goroutines.
- **Configurable timeout**: specify how long to wait for each connection.
- **JSON output**: easy to pipe into other tools or scripts.
- **Zero external dependencies** â pure Go standard library.

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-concurrent-ping-sweeper

# Build the binary
go build -o ping-sweeper ./src/main.go
```

The binary will be named `ping-sweeper` (or `ping-sweeper.exe` on Windows).

## Usage

```bash
./ping-sweeper -t 5 host1.example.com:80 host2.example.com:443 10.0.0.1:22
```

- `-t` â timeout in seconds for each connection (default: 3).
- Hosts are supplied as `address:port` strings.

### Example Output

```json
{
  "host1.example.com:80": 12.3,
  "host2.example.com:443": 45.7,
  "10.0.0.1:22": 0
}
```

The values are latency in milliseconds. A value of `0` indicates the host was unreachable or timed out.

## Testing

```bash
go test ./tests
```

The test suite uses a mock dialer to ensure deterministic, offline tests.

## License

MIT â see the repository LICENSE file.

