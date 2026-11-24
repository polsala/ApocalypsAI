## nightly-go-concurrency-probe

A whimsical yet useful Go utility designed to probe a list of network services concurrently. It reports the status of each service, indicating whether it's reachable or not.

### Philosophy

Embrace the power of Go's concurrency primitives to build robust and efficient network tools. This utility aims to be a simple, yet effective, way to monitor the health of your services.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrency_probe src/main.go
    ```

2.  **Run the utility:**
    Provide a list of host:port combinations as command-line arguments.
    ```bash
    ./concurrency_probe google.com:80 example.com:443 localhost:9090
    ```

### Output

The utility will output the status of each probed service:

```
Service google.com:80 is UP
Service example.com:443 is UP
Service localhost:9090 is DOWN
```

### Testing

Automated tests are included to ensure the utility functions correctly. These tests use mock network responses to remain deterministic and offline.

To run tests:

```bash
cd tests
go test
```
