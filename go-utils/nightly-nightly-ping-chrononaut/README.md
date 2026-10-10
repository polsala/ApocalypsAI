# nightly-ping-chrononaut

**A whimsical concurrent Go tool that simulates ping latencies for a list of hosts and displays a summary.**

## What it does

- Accepts any number of hostnames or IP addresses as command‑line arguments.
- Calculates a *deterministic* fake latency for each host (so the results are repeatable and testable).
- Runs the calculations concurrently using goroutines, showcasing Go's lightweight concurrency model.
- Prints a tidy table of "latency" values in milliseconds.

The utility is purely simulated – no real network traffic is generated – making it safe to run anywhere, even in offline CI environments.

## Installation

```bash
# Clone the repository (or copy the generated folder) and cd into it
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-ping-chrononaut

# Build the binary
go build -o ping-chrononaut ./src/main.go
```

## Usage

```bash
./ping-chrononaut example.com localhost 8.8.8.8
```

Sample output:

```
Simulated Ping Results:
example.com: 73 ms
localhost: 84 ms
8.8.8.8: 68 ms
```

## How latency is calculated

The latency is a simple deterministic function based on the host string:

```go
func computeLatency(host string) int {
    sum := 0
    for _, r := range host {
        sum += int(r)
    }
    return (sum % 100) + 20 // yields a value between 20‑119 ms
}
```

Because the algorithm depends only on the characters of the host name, the same input always yields the same output – perfect for unit tests.

## Testing

Run the tests with the standard Go toolchain:

```bash
go test ./tests
```

All tests are deterministic and do not perform any real network I/O.

## License

MIT © ApocalypsAI community
