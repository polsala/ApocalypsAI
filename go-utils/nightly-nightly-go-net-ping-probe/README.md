## Nightly Go Net Ping Probe

This utility is a standalone Go program designed to concurrently ping a list of network hosts and report their reachability status. It's useful for quick network health checks or monitoring a set of critical endpoints.

### Features

*   **Concurrent Pinging**: Utilizes Go's goroutines to ping multiple hosts simultaneously, significantly speeding up checks.
*   **Configurable Timeout**: Allows setting a timeout for each ping request.
*   **Clear Output**: Provides a simple, human-readable output of which hosts are reachable and which are not.
*   **Error Handling**: Gracefully handles network errors and timeouts.

### Usage

1.  **Build the utility**: 
    ```bash
    go build -o ping-probe src/main.go
    ```

2.  **Run the utility**: 
    The utility expects a list of hosts as command-line arguments. 
    ```bash
    ./ping-probe google.com example.com nonexistentsite.local 192.168.1.254
    ```

    You can also specify a timeout (in seconds) using the `-timeout` flag:
    ```bash
    ./ping-probe -timeout 2 google.com example.com
    ```

### Example Output

```
Host: google.com - Status: Reachable
Host: example.com - Status: Reachable
Host: nonexistentsite.local - Status: Unreachable (timeout)
Host: 192.168.1.254 - Status: Unreachable (timeout)
```

### Testing

Automated tests are included to verify the functionality. Run them using:

```bash
go test ./tests
```

These tests use mocked network responses to ensure deterministic and offline execution.
