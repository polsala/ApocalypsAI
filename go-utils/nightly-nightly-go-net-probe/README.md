## nightly-go-net-probe

A whimsical yet useful Go utility designed to concurrently probe a list of network endpoints. It reports on their availability and measures the latency of successful connections.

### Philosophy

In the chaotic aftermath, knowing which communication lines are still open is paramount. This tool provides a quick, concurrent way to check the pulse of your network infrastructure, ensuring vital connections remain active.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o netprobe src/main.go
    ```

2.  **Run the utility:**
    Provide a list of endpoints as command-line arguments.
    ```bash
    ./netprobe google.com:80 example.com:443 nonexistentsite.invalid:8080
    ```

### Output

The utility will output the status of each probed endpoint, including whether it was reachable and the round-trip time (latency) if successful.

```
Probing google.com:80...
  -> Reachable (Latency: 50ms)
Probing example.com:443...
  -> Reachable (Latency: 75ms)
Probing nonexistentsite.invalid:8080...
  -> Unreachable (Error: dial tcp: lookup nonexistentsite.invalid: no such host)
```

### Contributing

Contributions are welcome! Please ensure any new features or bug fixes are accompanied by comprehensive tests.
