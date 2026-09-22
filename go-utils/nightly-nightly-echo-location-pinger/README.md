# Nightly Echo-Location Pinger

## Overview

The `nightly-echo-location-pinger` is a whimsical-yet-useful utility designed to help you assess the reachability and latency of multiple network targets concurrently. It acts like a digital sonar, sending out 'pings' (TCP connection attempts) to specified hosts and ports, then reporting on the 'echoes' it receives.

This tool is ideal for quickly checking the status of multiple services, servers, or network devices in a distributed environment.

## Features

*   **Concurrent Pinging**: Utilizes Go's goroutines to check multiple targets simultaneously.
*   **TCP Port Reachability**: Attempts to establish a TCP connection to a specified host and port.
*   **Latency Measurement**: Reports the time taken for each successful or failed connection attempt.
*   **Customizable Timeout**: Allows specifying a global timeout for all ping operations.
*   **Clear Output**: Provides a structured report of each target's status, latency, and any errors.

## Installation

To build and run this utility, you need Go (version 1.16 or higher) installed.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-echo-location-pinger
    ```
2.  **Build the executable:**
    ```bash
    go build -o echo-pinger src/main.go
    ```

## Usage

Run the compiled executable with a list of targets (host:port) and an optional global timeout.

```bash
./echo-pinger <target1> [target2...] [--timeout=<duration>]
```

*   `<target>`: The host and port to ping, e.g., `google.com:80`, `192.168.1.1:22`.
*   `--timeout=<duration>`: Optional. The maximum time to wait for a connection attempt. Defaults to `5s` (5 seconds). Duration can be specified as `100ms`, `1s`, `5s`, `1m`, etc.

### Examples

**1. Ping Google's HTTP and SSH on a local machine with default timeout:**

```bash
./echo-pinger google.com:80 127.0.0.1:22
```

**2. Ping multiple services with a custom 500ms timeout:**

```bash
./echo-pinger example.com:443 mydatabase:5432 mycache:6379 --timeout=500ms
```

**3. Ping a single target:**

```bash
./echo-pinger api.service.com:8080
```

## Output

The utility will print a report to standard output, detailing the status of each target:

```
--- Echo-Location Report ---
Target: google.com:80         Status: Success  Latency: 12.345ms
Target: 127.0.0.1:22          Status: Failed   Error: dial tcp 127.0.0.1:22: connect: connection refused
Target: example.com:443       Status: Success  Latency: 25.678ms
--------------------------
```

## Development

### Running Tests

To run the automated tests, navigate to the utility's root directory and execute:

```bash
go test ./tests/...
```

Tests are designed to be deterministic and run offline by mocking network operations using Go's variable-based mocking strategy for `net.DialTimeout`.
