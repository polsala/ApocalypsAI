## Nightly Go Concurrent Ping

This utility allows you to ping multiple network hosts concurrently using Go's powerful concurrency features. It's designed to be fast and efficient, providing a quick overview of network connectivity.

### Features

*   **Concurrent Pinging**: Utilizes goroutines to ping multiple hosts simultaneously.
*   **Configurable Timeout**: Set a custom timeout for each ping request.
*   **Clear Output**: Displays the status (up/down) and response time for each host.
*   **Error Handling**: Gracefully handles network errors and unreachable hosts.

### Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-ping main.go
    ```

2.  **Run with hosts**: 
    ```bash
    ./concurrent-ping google.com 8.8.8.8 invalid.host 1.1.1.1
    ```

3.  **Run with a timeout (e.g., 2 seconds)**:
    ```bash
    ./concurrent-ping -timeout=2s google.com 8.8.8.8 invalid.host 1.1.1.1
    ```

### Configuration

The utility accepts a single optional flag `-timeout` to specify the ping timeout duration. The default timeout is 1 second.

### Development

This utility is built using Go and leverages its standard library for networking and concurrency.

### Tests

Automated tests are included to verify the functionality of the ping utility. These tests use mocks to ensure deterministic and offline execution.
