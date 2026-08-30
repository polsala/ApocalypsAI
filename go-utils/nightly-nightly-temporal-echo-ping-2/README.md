# Nightly Temporal Echo Ping

## Overview

The `nightly-temporal-echo-ping` is a Go utility designed to monitor the "temporal stability" of various network endpoints, referred to as "temporal anchors." It concurrently pings a list of specified URLs or IP addresses, measuring their response times and reporting on latency, minimum, maximum, and average response times, as well as any encountered errors.

This tool is useful for quickly assessing the health and responsiveness of critical services or infrastructure components in a distributed or post-apocalyptic network environment.

## Features

*   **Concurrent Pinging**: Utilizes Go's goroutines to ping multiple targets simultaneously.
*   **Latency Metrics**: Reports minimum, maximum, and average latency for each target.
*   **Error Reporting**: Clearly indicates targets that failed to respond or timed out.
*   **Configurable**: Allows specifying targets, ping count, and timeout duration via command-line flags.

## Installation

To build and run this utility, you need Go (version 1.16 or higher) installed.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-temporal-echo-ping
    ```
2.  **Build the executable:**
    ```bash
    go build -o temporal-echo-ping src/main.go
    ```

## Usage

Run the compiled executable or use `go run` directly.

```bash
./temporal-echo-ping -targets "http://example.com,http://google.com" -count 3 -timeout 5s
```

### Command-line Flags

*   `-targets <URL1,URL2,...>`: A comma-separated list of URLs or IP addresses to ping. (Required)
*   `-count <int>`: The number of times to ping each target. (Default: `1`)
*   `-timeout <duration>`: The maximum time to wait for a response for each ping (e.g., `1s`, `500ms`). (Default: `3s`)

### Example Output

```
Initiating Temporal Echo Pings...

--- Ping Statistics for http://example.com ---
  Pings Sent: 3
  Successful: 3
  Failed: 0
  Min Latency: 123.45ms
  Max Latency: 150.21ms
  Avg Latency: 135.88ms

--- Ping Statistics for http://nonexistent.invalid ---
  Pings Sent: 3
  Successful: 0
  Failed: 3
  Errors: 
    Get "http://nonexistent.invalid": dial tcp: lookup nonexistent.invalid: no such host
    Get "http://nonexistent.invalid": dial tcp: lookup nonexistent.invalid: no such host
    Get "http://nonexistent.invalid": dial tcp: lookup nonexistent.invalid: no such host

Temporal Echo Pings Complete.
```

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
go test ./tests/...
```
