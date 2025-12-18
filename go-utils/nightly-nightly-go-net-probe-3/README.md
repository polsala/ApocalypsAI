## nightly-go-net-probe

A whimsical yet useful Go utility designed to concurrently probe a list of network endpoints. It reports on their reachability and measures the latency to each.

### Philosophy

In the chaotic aftermath, knowing which communication lines are still open is paramount. This tool provides a quick, concurrent way to check the pulse of your network.

### Usage

1.  **Build:**
    ```bash
    go build -o netprobe ./src/main.go
    ```

2.  **Run:**
    Provide a list of endpoints (host:port or IP:port) as command-line arguments.
    ```bash
    ./netprobe google.com:80 example.com:443 192.168.1.1:22
    ```

    You can also specify a timeout duration (in seconds) using the `-timeout` flag:
    ```bash
    ./netprobe -timeout 5 google.com:80 example.com:443
    ```

### Output

The utility will output a line for each probed endpoint, indicating:
-   The endpoint address.
-   Whether it was reachable (`UP` or `DOWN`).
-   The round-trip time (latency) if reachable.

### Example Output

```
Endpoint: google.com:80, Status: UP, Latency: 25ms
Endpoint: example.com:443, Status: UP, Latency: 40ms
Endpoint: 192.168.1.1:22, Status: DOWN, Latency: N/A
```

### Testing

Run the tests using Go's built-in testing framework:
```bash
cd tests
go test
```

### Contributing

This is a community utility. Feel free to fork, improve, and submit pull requests!
