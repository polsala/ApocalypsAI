# Nightly Reality Anchor Pinger

## Overview

The `nightly-reality-anchor-pinger` is a whimsical-yet-useful utility designed to concurrently check the network stability and latency of a list of specified "reality anchors" (network hosts). In a world where digital stability is paramount, this tool helps you ensure your critical network endpoints are reachable and responsive.

It uses Go's concurrency features to ping multiple hosts simultaneously, providing a quick overview of your network's health.

## Features

*   **Concurrent Pinging**: Checks multiple hosts at once using Go goroutines.
*   **Configurable Port**: Specify the TCP port to connect to (default: 80).
*   **Configurable Timeout**: Set a custom timeout for each ping attempt (default: 5 seconds).
*   **Detailed Report**: Outputs the status and latency for each anchor.
*   **Exit Code**: Exits with a non-zero code if any anchor fails to respond, useful for CI/CD or monitoring scripts.

## Usage

### Prerequisites

To run this utility, you need Go installed (version 1.16 or higher).

### Building from Source

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-reality-anchor-pinger
go build -o reality-anchor-pinger src/main.go
```

### Running the Utility

Run the compiled executable with a list of hosts. You can also specify a custom port and timeout.

```bash
./reality-anchor-pinger <host1> [host2...] [--port=<port>] [--timeout=<duration>]
```

**Examples:**

1.  **Ping Google and Cloudflare DNS on default HTTP port (80) with default timeout (5s):**
    ```bash
    ./reality-anchor-pinger google.com 1.1.1.1
    ```

2.  **Ping a custom server on port 22 (SSH) with a 2-second timeout:**
    ```bash
    ./reality-anchor-pinger my-server.example.com --port=22 --timeout=2s
    ```

3.  **Ping multiple hosts on HTTPS port (443):**
    ```bash
    ./reality-anchor-pinger github.com api.example.com --port=443
    ```

## Output Example

```
Pinging 3 reality anchors on port 80 with timeout 5s...

--- Reality Anchor Stability Report ---
  google.com:80 - OK (Latency: 12.345ms)
  nonexistent.domain:80 - FAILED (dial tcp: lookup nonexistent.domain: no such host)
  8.8.8.8:80 - OK (Latency: 25.678ms)
-------------------------------------
```

## Development

### Running Tests

To run the unit tests, navigate to the utility's directory and execute:

```bash
go test ./tests/...
```

The tests use a mock `Pinger` interface to simulate network responses, ensuring deterministic and offline testing.
