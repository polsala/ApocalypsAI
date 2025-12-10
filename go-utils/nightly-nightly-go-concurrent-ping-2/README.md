## Nightly Go Concurrent Ping

A whimsical yet useful Go utility designed to concurrently ping multiple network hosts. It's perfect for quickly checking the reachability of a list of servers, especially in a post-apocalyptic scenario where reliable communication is key.

### Features

*   **Concurrency**: Utilizes Go's goroutines to ping multiple hosts simultaneously, maximizing efficiency.
*   **Configurable Timeout**: Set a custom timeout for each ping request.
*   **Clear Output**: Presents results in an easy-to-read format, indicating success or failure for each host.
*   **Error Handling**: Gracefully handles network errors and timeouts.

### Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-ping main.go
    ```

2.  **Run the utility**: 
    Provide a list of hosts as command-line arguments.
    ```bash
    ./concurrent-ping google.com example.com nonexistentserver.local
    ```

    You can also specify a timeout (in seconds) using the `-timeout` flag:
    ```bash
    ./concurrent-ping -timeout 2 google.com example.com nonexistentserver.local
    ```

### Example Output

```
Pinging google.com (142.250.184.142)...
  Success: google.com is reachable.

Pinging example.com (93.184.216.34)...
  Success: example.com is reachable.

Pinging nonexistentserver.local...
  Failed: nonexistentserver.local: lookup nonexistentserver.local: no such host (timeout: 1s)
```

### Testing

Run the tests using Go's built-in testing framework:
```bash
go test -v ./...
```
