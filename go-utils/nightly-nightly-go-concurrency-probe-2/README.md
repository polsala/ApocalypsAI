# Go Concurrency Probe (nightly-go-concurrency-probe)

This utility is a whimsical yet useful Go program designed to probe a list of network services concurrently. It's built to be a standalone tool for quickly checking the availability of multiple endpoints without overwhelming your system.

## Philosophy

Inspired by the need for rapid, concurrent network checks in a potentially chaotic environment, this tool leverages Go's powerful concurrency primitives to provide efficient service status updates.

## Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrency_probe src/main.go
    ```

2.  **Run the utility:**
    The utility expects a list of host:port targets as command-line arguments.

    ```bash
    ./concurrency_probe google.com:80 example.com:443 localhost:8080
    ```

    **Example Output:**
    ```
    [2023-10-27 10:00:00] Probing google.com:80...
    [2023-10-27 10:00:00] google.com:80 is UP
    [2023-10-27 10:00:00] Probing example.com:443...
    [2023-10-27 10:00:00] example.com:443 is UP
    [2023-10-27 10:00:00] Probing localhost:8080...
    [2023-10-27 10:00:01] localhost:8080 is DOWN (connection refused)
    ```

## How it Works

The `main.go` program takes a variable number of host:port strings as arguments. For each target, it launches a goroutine that attempts to establish a TCP connection. A timeout is applied to each connection attempt to prevent indefinite hangs. The results (UP or DOWN with an error message) are printed to standard output.

## Testing

Automated tests are included to verify the functionality of the probing logic. These tests use mocked network responses to ensure deterministic and offline execution.

To run the tests:

```bash
    go test ./tests/...
    ```
