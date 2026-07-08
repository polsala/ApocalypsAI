# Go Network Probe (nightly-go-net-probe)

A whimsical yet useful Go utility designed to concurrently probe a list of network endpoints, reporting on their availability and latency. It's built with the spirit of the ApocalypsAI in mind – robust, efficient, and ready for anything.

## Features

*   **Concurrent Probing**: Utilizes Go's goroutines to check multiple endpoints simultaneously.
*   **Configurable Targets**: Define a list of URLs or IP addresses to probe.
*   **Latency Measurement**: Reports the time taken to receive a response.
*   **Status Reporting**: Indicates whether an endpoint is reachable or not.
*   **Simple CLI Interface**: Easy to use from the command line.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o netprobe src/main.go
    ```

2.  **Run the utility**: 
    The utility expects a list of targets as command-line arguments.
    ```bash
    ./netprobe https://www.google.com http://localhost:8080 https://example.com
    ```

    You can also redirect a file containing targets:
    ```bash
    ./netprobe < targets.txt
    ```

## Example `targets.txt`

```
https://www.github.com
http://127.0.0.1:9000
https://api.openai.com
```

## How it Works

The `main.go` program iterates through provided targets. For each target, it launches a goroutine that performs an HTTP GET request (or a TCP dial for non-HTTP URLs). It measures the time taken for the request and reports the status (OK/Error) and latency.

## Testing

Automated tests are included to ensure the utility functions correctly. These tests use mocks to simulate network responses without requiring actual network connectivity.

To run tests:
```bash
cd tests
go test
```
