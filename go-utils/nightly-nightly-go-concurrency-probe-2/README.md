# Go Concurrency Probe

This utility is a whimsical yet useful Go program designed to concurrently probe a list of network services (specified by host:port) and report their availability. It leverages Go's powerful concurrency features to perform multiple checks simultaneously, making it efficient for monitoring a set of services.

## Philosophy

Inspired by the need for quick, reliable network checks in a potentially chaotic environment, this tool embraces Go's strengths in building concurrent network applications. It's designed to be simple, effective, and easy to run.

## Features

*   **Concurrent Probing**: Uses goroutines to check multiple hosts simultaneously.
*   **Configurable Timeout**: Set a timeout for each probe to avoid hanging.
*   **Clear Output**: Reports which services are up and which are down.
*   **Standalone Binary**: Compiles into a single executable.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrency_probe src/main.go
    ```

2.  **Run the utility**: 
    The utility expects a list of `host:port` targets as command-line arguments.
    ```bash
    ./concurrency_probe google.com:80 example.com:443 localhost:9000
    ```

    You can also specify a timeout (in seconds) using the `-timeout` flag:
    ```bash
    ./concurrency_probe -timeout 2 google.com:80 example.com:443 localhost:9000
    ```

## How it Works

The `main.go` file defines a `probeService` function that attempts to establish a TCP connection to a given `host:port`. This function is then executed as a goroutine for each target. A channel is used to collect the results (whether the service is up or down), and a `sync.WaitGroup` ensures that all goroutines complete before the program exits.

## Testing

Automated tests are included to verify the functionality of the `probeService` function using mocked network responses. To run the tests:

```bash
go test -v ./tests/...
```
