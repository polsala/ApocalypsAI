# nightly-concurrent-ping

## Overview

`nightly-concurrent-ping` is a tiny Go command‑line utility that pings a list of hosts **concurrently** using a TCP connection to port 80. It measures how long each connection takes (or reports the host as unreachable) and prints a simple summary, including the average latency of all reachable hosts.

The tool is deliberately whimsical – it pretends to be a “post‑apocalyptic network scanner” – but it is also genuinely useful for quick latency checks without installing external tools like `ping` or `curl`.

## Installation

```bash
# Clone the repository (or copy the generated files into your project)
git clone https://github.com/your-org/ApocalypsAI.git
cd utils/nightly-concurrent-ping

# Build the binary (requires Go 1.22 or later)
go build -o nightly-concurrent-ping ./src/main.go
```

## Usage

```bash
./nightly-concurrent-ping host1.example.com 8.8.8.8 localhost
```

Sample output:

```
host1.example.com: 84.3ms
8.8.8.8: 27.1ms
localhost: 0.5ms
Average latency: 37.3ms
```

If a host cannot be reached within the 2‑second timeout, it is reported as `unreachable` and excluded from the average calculation.

## How it works

* **Concurrency** – Each host is pinged in its own goroutine, allowing dozens of hosts to be checked in parallel.
* **Pluggable provider** – The core logic depends on a `PingProvider` interface. The production implementation performs a real TCP dial, while the test suite injects a mock provider for deterministic results.
* **Deterministic tests** – The test suite replaces the network layer with a mock that returns predefined latencies, ensuring the tests run offline and are repeatable.

## Testing

```bash
go test ./tests
```

The test suite validates that the concurrent ping logic correctly aggregates results and handles unreachable hosts.

## License

MIT © ApocalypsAI
