A whimsical yet useful standalone utility for the ApocalypsAI community.

## nightly-go-net-probe

This utility, built with Go, allows you to concurrently probe a list of network endpoints (URLs or IP addresses) to check their availability and measure their response times. It's designed to be fast and efficient, leveraging Go's concurrency features.

### Philosophy

"Measure twice, probe once." This tool aims to provide a quick and reliable way to get a snapshot of network health, whether for monitoring your own services or checking external dependencies.

### Usage

Compile the Go program and run it from your terminal.

```bash
go build -o netprobe src/main.go
./netprobe --targets "http://google.com,https://example.com,1.1.1.1:53"
```

**Arguments:**

*   `--targets`: A comma-separated list of network endpoints to probe. Supports URLs (e.g., `http://example.com`) and IP:Port combinations (e.g., `1.1.1.1:53`).
*   `--timeout`: (Optional) The timeout in seconds for each probe. Defaults to 5 seconds.
*   `--concurrency`: (Optional) The maximum number of concurrent probes. Defaults to 10.

### Output

The utility will print the status (UP/DOWN) and the response time (in milliseconds) for each probed endpoint.

```
[INFO] Probing http://google.com...
[INFO] http://google.com is UP (25ms)
[INFO] Probing https://example.com...
[INFO] https://example.com is UP (15ms)
[INFO] Probing 1.1.1.1:53...
[INFO] 1.1.1.1:53 is UP (30ms)
```

### Contributing

Feel free to fork this repository and submit pull requests with improvements or new features. All contributions are welcome!
