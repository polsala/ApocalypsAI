# Nightly WhisperNet Amplifier

## Summary

The `nightly-whispernet-amplifier` is a whimsical-yet-useful Go utility designed to monitor the network connectivity and responsiveness of a list of specified URLs or IP addresses. It uses Go's concurrency features (goroutines) to check multiple 'critical nodes' simultaneously, reporting their 'WhisperNet Signal Strength' with fun, thematic status messages and latency details.

This tool is perfect for quickly assessing the health of your essential services or external dependencies, presented with a touch of post-apocalyptic charm.

## Features

*   **Concurrent Monitoring**: Checks multiple targets in parallel for speed.
*   **Whimsical Statuses**: Reports connectivity using 'Signal Strong', 'Faint Echo', 'Lost in the Static', and other thematic messages.
*   **Latency Reporting**: Provides response times for each node.
*   **HTTP Status Codes**: Includes the HTTP status code for successful (or error) responses.
*   **Configurable Timeout**: Uses a default timeout for network requests to prevent indefinite waits.

## How to Build

1.  **Ensure Go is installed**: You need Go 1.16 or newer. If not, download it from [golang.org](https://golang.org/dl/).
2.  **Navigate to the utility directory**: `cd go-utils/nightly-whispernet-amplifier`
3.  **Build the executable**: `go build -o nightly-whispernet-amplifier src/main.go`

This will create an executable named `nightly-whispernet-amplifier` in the current directory.

## How to Run

Run the executable followed by the URLs or IP addresses you wish to monitor:

```bash
./nightly-whispernet-amplifier https://google.com http://localhost:8080 https://api.example.com/health
```

### Example Output

```
--- WhisperNet Signal Amplifier Report ---
Scanning 3 critical nodes...

Node: https://google.com
  Status: Signal Strong
  Latency: 123.45ms
  HTTP Code: 200
----------------------------------------
Node: http://localhost:8080
  Status: Lost in the Static (Connection Refused) (dial tcp 127.0.0.1:8080: connect: connection refused)
  Latency: 1.23ms
----------------------------------------
Node: https://api.example.com/health
  Status: Faint Echo (Client Error)
  Latency: 56.78ms
  HTTP Code: 404
----------------------------------------

--- Scan Complete ---
```

## Development & Testing

### Running Tests

To run the automated tests, navigate to the utility directory and execute:

```bash
go test ./tests/test_main.go
```

All tests are designed to be deterministic and run offline using Go's `httptest` package to mock HTTP servers, simulating various network conditions without external dependencies.
