## nightly-go-net-probe

A whimsical yet useful Go utility designed to concurrently probe a list of network endpoints. It reports on their reachability and measures the latency of successful connections.

### Philosophy

In the chaotic aftermath, knowing which communication lines are still open is paramount. This tool provides a swift, concurrent way to check the pulse of your network infrastructure, ensuring vital connections remain intact.

### Usage

1.  **Build:**
    ```bash
    go build -o netprobe src/main.go
    ```

2.  **Run:**
    Provide a list of endpoints (host:port or IP:port) as command-line arguments.
    ```bash
    ./netprobe example.com:80 google.com:443 192.168.1.1:22
    ```

### Output

The utility will print the status of each probed endpoint, including whether it was reachable and, if so, the round-trip time (latency) in milliseconds.

Example:

```
Probing example.com:80... Reachable (Latency: 55ms)
Probing google.com:443... Reachable (Latency: 32ms)
Probing 192.168.1.1:22... Unreachable
```

### Features

*   **Concurrency:** Utilizes Go's goroutines to probe multiple endpoints simultaneously.
*   **Error Handling:** Gracefully handles connection errors and timeouts.
*   **Latency Measurement:** Reports latency for successful connections.
*   **Simple CLI:** Easy to use with command-line arguments.

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
