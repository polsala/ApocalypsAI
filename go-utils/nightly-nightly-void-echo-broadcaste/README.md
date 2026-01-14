# nightly-void-echo-broadcaster

A concurrent Go utility that simulates broadcasting echo messages across a distributed network of wasteland outposts. Designed for fun and testing inter-node communication in post-apocalyptic scenarios.

## Features

- Concurrent message broadcasting
- Simulated network latency and packet loss
- Configurable echo intensity and delay
- CLI interface for easy testing

## Usage

```bash
# Build the utility
go build -o broadcaster src/main.go

# Run with default settings
./broadcaster

# Run with custom settings
./broadcaster --nodes=5 --delay=200ms --loss=10
```

## Options

- `--nodes`: Number of simulated network nodes (default: 3)
- `--delay`: Base network delay per node (default: 100ms)
- `--loss`: Simulated packet loss percentage (default: 5)

## Example Output

```
[Node 1] Broadcasting: "Echo from the void..."
[Node 2] Received: "Echo from the void..." (delay: 120ms)
[Node 3] Received: "Echo from the void..." (delay: 95ms)
```
