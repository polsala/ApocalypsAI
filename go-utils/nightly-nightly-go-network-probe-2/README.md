# Go Network Probe

This utility is a whimsical yet useful tool written in Go that allows you to concurrently probe a list of network endpoints (URLs or IP addresses) to check their reachability and measure the latency of successful connections.

## Philosophy

Inspired by the need for quick, reliable network diagnostics in a potentially chaotic world, this tool embraces Go's concurrency features to provide fast and efficient probing.

## Features

*   **Concurrent Probing**: Utilizes goroutines to probe multiple endpoints simultaneously.
*   **HTTP/HTTPS and TCP Support**: Can probe web endpoints (HTTP/HTTPS) and raw TCP ports.
*   **Latency Measurement**: Reports the time taken for a successful connection.
*   **Configurable Timeout**: Set a timeout for each probe to avoid hanging.
*   **Clear Output**: Presents results in an easy-to-read format.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o network-probe src/main.go
    ```

2.  **Run the utility**: 
    Provide a list of endpoints as command-line arguments. Endpoints can be URLs (e.g., `https://example.com`, `http://localhost:8080`) or TCP addresses (e.g., `192.168.1.1:22`).

    ```bash
    ./network-probe https://google.com http://localhost:8080 1.1.1.1:53 --timeout 5s
    ```

    **Options**: 
    *   `--timeout <duration>`: Sets the maximum time to wait for a probe to complete (e.g., `5s`, `1m`). Defaults to `10s`.

## Example Output

```
Probing endpoints...

[SUCCESS] https://google.com (142.250.184.142:443) - Latency: 85ms
[FAILURE] http://localhost:8080 - Error: dial tcp 127.0.0.1:8080: connect: connection refused
[SUCCESS] 1.1.1.1:53 (1.1.1.1:53) - Latency: 25ms
```

## Development

This utility is written in Go and leverages its standard library for networking and concurrency.

## Testing

Automated tests are included to verify the functionality of the probe. These tests use mocked network responses to ensure deterministic and offline execution.
