# nightly-concurrent-ping-sweeper

A whimsical yet useful Go utility that pings multiple hosts concurrently by opening a short‑lived TCP connection to port 80, measures the round‑trip latency, and prints the results sorted from fastest to slowest.

## Features

- **Concurrent**: launches a goroutine per host, making full use of Go's lightweight concurrency.
- **Deterministic output**: prints each host with its measured latency (or error) in a tidy table.
- **Testable**: the networking layer is abstracted so unit tests can mock latency values without real network traffic.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-concurrent-ping-sweeper
go build -o ping-sweeper ./src/main.go
```

## Usage

```bash
# Pass a list of hostnames or IP addresses as arguments
./ping-sweeper example.com google.com 8.8.8.8
```

Output example:

```
example.com    45.2ms
google.com     78.9ms
8.8.8.8       112.3ms
```

If a host cannot be reached, the error is shown instead of a latency:

```
nonexistent.tld    error: dial tcp: lookup nonexistent.tld: no such host
```

## Testing

Run the unit tests with:

```bash
go test ./tests
```

The tests use a mock dialer, so they run offline and deterministically.
