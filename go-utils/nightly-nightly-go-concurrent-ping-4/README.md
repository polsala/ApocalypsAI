## Nightly Go Concurrent Ping

This utility allows you to concurrently ping multiple network hosts and get a quick overview of their reachability. It's built with Go to leverage its excellent concurrency primitives for efficient network operations.

### Features

*   **Concurrent Pinging**: Pings multiple hosts simultaneously using goroutines.
*   **Configurable Timeout**: Set a timeout for each ping request.
*   **Clear Output**: Displays the status (reachable/unreachable) for each host.
*   **Error Handling**: Gracefully handles network errors.

### Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-ping src/main.go
    ```

2.  **Run the utility**: 
    Provide a list of hosts as command-line arguments. For example:
    ```bash
    ./concurrent-ping google.com github.com nonexistentsite.local 192.168.1.254
    ```

    You can also specify a timeout in seconds using the `-timeout` flag:
    ```bash
    ./concurrent-ping -timeout 2 google.com github.com nonexistentsite.local
    ```

### How it Works

The `main.go` file defines a `pingHost` function that attempts to establish a TCP connection to the specified host and port (defaulting to port 80 for HTTP, but the ping itself is a basic network reachability check). It uses a `context` with a timeout to limit the duration of each ping attempt. Multiple `pingHost` calls are launched as goroutines, allowing for parallel execution. The results are collected and printed to the console.

### Testing

Automated tests are included to verify the functionality of the `pingHost` function. These tests use mocked network responses to ensure deterministic and offline execution.

To run the tests:
```bash
go test ./tests/...
```
