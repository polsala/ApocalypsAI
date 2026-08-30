# Nightly Reality Ripple Monitor

## Overview

The `nightly-reality-ripple-monitor` is a Go-based utility designed to concurrently monitor the 'reality ripple' of various critical network endpoints. In the post-apocalyptic landscape, network stability is paramount. This tool simulates sending out 'temporal pings' and listens for their echoes, reporting on the latency and availability of each target.

It's perfect for quickly assessing the health of your distributed services, ensuring your communication channels remain stable amidst temporal distortions.

## Features

*   **Concurrent Monitoring**: Utilizes Go's goroutines to check multiple URLs simultaneously.
*   **Latency Measurement**: Reports the time taken for each 'ripple' to return.
*   **Status Reporting**: Indicates `OK`, `FAILED` (network error), `TIMEOUT`, or specific HTTP error codes.
*   **Configurable Timeout**: Prevents indefinite waits for unresponsive endpoints.

## Usage

### Build

First, clone the repository and navigate to the utility's directory:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-reality-ripple-monitor
```

Then, build the executable:

```bash
go build -o reality-ripple-monitor src/main.go
```

### Run

Execute the compiled binary with a list of URLs to monitor. Each URL will be checked concurrently.

```bash
./reality-ripple-monitor https://example.com https://api.myservice.com/health http://localhost:8080/status
```

**Example Output:**

```
Monitoring 3 endpoints...

--- Reality Ripple Report ---
[OK] https://example.com (Latency: 123.45ms)
[ERROR 404] https://api.myservice.com/health (Latency: 56.78ms)
[FAILED] http://localhost:8080/status (Error: connection refused) (Latency: 0.12ms)

Overall Status: Some ripples are unstable.
```

### Arguments

Simply provide the URLs as command-line arguments. The utility expects at least one URL.

## Development

### Tests

To run the tests, navigate to the utility's directory and execute:

```bash
go test ./tests/...
```

Tests are designed to be deterministic and offline, using a mock HTTP client to simulate various network responses, errors, and latencies without making actual network calls.
