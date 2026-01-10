# nightly-void-latency-monitor

A whimsical-yet-useful utility to monitor the "temporal stability" of various "void" network endpoints by measuring TCP connection latency. Ever wondered if the fabric of reality is tearing? This tool provides a highly scientific (and slightly dramatic) report on your network's connection health to critical, imaginary infrastructure.

## Usage

### Build

Navigate to the `src` directory and build the Go executable:

```bash
cd src
go build -o void-latency-monitor .
```

### Run

Execute the compiled binary. By default, it monitors a few predefined "void" endpoints.

```bash
./void-latency-monitor
```

Example Output:

```
Initiating Void Latency Monitoring...
Monitoring 3 endpoints, 3 pings each, with 2s timeout.

--- Void Latency Report ---

Endpoint: The Void (example.com:80)
  Pings Sent: 3
  Successful: 3 (100.00%)
  Avg Latency: 15.23ms
  Min Latency: 12.11ms
  Max Latency: 18.35ms
  Temporal Stability: HIGH - The Void is calm.

Endpoint: Temporal Rift Gateway (nonexistent.invalid:80)
  Pings Sent: 3
  Successful: 0 (0.00%)
  No successful pings.
  Temporal Stability: LOW - The fabric of reality is tearing!

Endpoint: Echo Chamber Nexus (google.com:443)
  Pings Sent: 3
  Successful: 3 (100.00%)
  Avg Latency: 25.67ms
  Min Latency: 23.45ms
  Max Latency: 28.99ms
  Temporal Stability: HIGH - The Void is calm.
```

## Development

### Running Tests

Navigate to the `tests` directory and run the Go tests:

```bash
cd tests
go test -v .
```

The tests use a mock `Pinger` implementation to simulate network responses, ensuring deterministic and offline execution.
