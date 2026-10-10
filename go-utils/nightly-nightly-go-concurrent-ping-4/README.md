## Nightly Go Concurrent Ping

A whimsical yet useful utility written in Go that allows you to concurrently ping a list of hosts and get a quick overview of their reachability. Perfect for network sanity checks in a post-apocalyptic world where reliable communication is key!

### Features

*   **Concurrent Pinging**: Utilizes Go's goroutines to ping multiple hosts simultaneously, significantly speeding up the process.
*   **Configurable Timeout**: Set a custom timeout for each ping attempt.
*   **Clear Output**: Displays the status (reachable or unreachable) for each host.
*   **Error Handling**: Gracefully handles network errors and timeouts.

### Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-ping src/main.go
    ```

2.  **Run with a list of hosts**: 
    The utility expects a list of hosts as command-line arguments. You can also specify a timeout duration (e.g., `500ms`, `1s`). If no timeout is provided, it defaults to `1s`.

    ```bash
    ./concurrent-ping google.com github.com nonexistentsite.local 1.1.1.1 500ms
    ```

    **Example Output**: 
    ```
    Pinging google.com...
    Pinging github.com...
    Pinging nonexistentsite.local...
    Pinging 1.1.1.1...
    
    Results:
    google.com: Reachable
    github.com: Reachable
    nonexistentsite.local: Unreachable
    1.1.1.1: Reachable
    ```

### Development Notes

This utility is built using Go, leveraging goroutines for concurrency. The `net.DialTimeout` function is used for pinging, which is a simple and effective way to check network connectivity without requiring root privileges.

### Testing

Automated tests are included to verify the functionality of the pinging logic and error handling. These tests are deterministic and do not require external network access.
