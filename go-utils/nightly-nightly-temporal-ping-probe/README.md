# Nightly Temporal Ping Probe

## Overview

The `nightly-temporal-ping-probe` is a whimsical-yet-useful Go utility designed to help the community observe "temporal drift" across their network infrastructure. In essence, it's a concurrent network reachability and latency checker that reports the connection status, latency, and the local timestamp of the probe for each target host and port.

While it doesn't directly synchronize time, by providing a consistent local timestamp with each probe result, it allows operators to manually compare results from different machines or over time, aiding in the detection of network issues or potential time synchronization discrepancies.

## Features

*   **Concurrent Probing**: Utilizes Go's goroutines to probe multiple hosts simultaneously for efficiency.
*   **Latency Measurement**: Reports the time taken to establish a TCP connection to the specified port.
*   **Reachability Status**: Clearly indicates whether a host:port combination is reachable or not.
*   **Local Timestamp**: Includes the exact local time when the probe was initiated, useful for correlating events or observing time drift.
*   **Configurable Timeout**: Uses a default 5-second timeout for connection attempts.

## Installation

To install the `nightly-temporal-ping-probe`, ensure you have Go (version 1.16 or higher) installed on your system.

1.  Clone the ApocalypsAI repository (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility's directory:
    ```bash
    cd go-utils/nightly-temporal-ping-probe
    ```
3.  Build the executable:
    ```bash
    go build -o temporal-ping-probe src/main.go
    ```

This will create an executable named `temporal-ping-probe` in the current directory.

## Usage

Run the utility from your terminal, providing the target port and a list of hostnames or IP addresses.

```bash
./temporal-ping-probe <port> <host1> [host2...]
```

### Arguments:

*   `<port>`: The TCP port number to probe on each host (e.g., 80 for HTTP, 443 for HTTPS, 22 for SSH).
*   `<host1> [host2...]`: One or more hostnames or IP addresses to probe.

### Examples:

1.  Probe a single host on port 80:
    ```bash
    ./temporal-ping-probe 80 example.com
    ```
    Expected Output:
    ```
    Host: example.com:80 | Status: REACHABLE | Latency: 12.34ms | Timestamp: 2023-10-27T10:30:00Z
    ```

2.  Probe multiple hosts on port 443:
    ```bash
    ./temporal-ping-probe 443 google.com github.com nonexistent.local
    ```
    Expected Output (order may vary due to concurrency):
    ```
    Host: google.com:443 | Status: REACHABLE | Latency: 25.67ms | Timestamp: 2023-10-27T10:30:01Z
    Host: github.com:443 | Status: REACHABLE | Latency: 30.12ms | Timestamp: 2023-10-27T10:30:01Z
    Host: nonexistent.local:443 | Status: UNREACHABLE | Latency: N/A | Timestamp: 2023-10-27T10:30:01Z
    ```

## Development

### Running Tests

To run the automated tests for this utility:

```bash
cd go-utils/nightly-temporal-ping-probe
go test ./tests/...
```

The tests use mock network components to ensure determinism and offline execution.
