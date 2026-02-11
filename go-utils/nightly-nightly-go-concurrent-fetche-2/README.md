# Nightly Go Concurrent Fetcher

This utility is a standalone Go program designed to fetch multiple URLs concurrently and report their HTTP status codes and response times. It's useful for quickly checking the health of a list of endpoints or for basic network diagnostics.

## Features

*   **Concurrency**: Utilizes Go's goroutines to fetch URLs in parallel.
*   **Timeout**: Configurable timeout for each HTTP request to prevent hanging.
*   **Status Reporting**: Displays the HTTP status code for each URL.
*   **Response Time**: Reports the time taken to receive a response.
*   **Error Handling**: Gracefully handles network errors and timeouts.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-fetcher src/main.go
    ```

2.  **Run with a list of URLs**: 
    The utility expects a list of URLs as command-line arguments. 
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com http://localhost:9999
    ```

3.  **With a timeout (in seconds)**: 
    You can specify a timeout for all requests using the `-timeout` flag.
    ```bash
    ./concurrent-fetcher -timeout 5s https://www.google.com https://www.github.com
    ```

## Example Output

```
Fetching: https://www.google.com
Fetching: https://www.github.com
Fetching: http://localhost:9999

Results:
- https://www.google.com: Status=200 OK, Time=150ms
- https://www.github.com: Status=200 OK, Time=220ms
- http://localhost:9999: Error=Get "http://localhost:9999": dial tcp 127.0.0.1:9999: connectex: No connection could be made because the target machine actively refused it., Time=5s (Timeout)
```

## Development

This utility is written in Go and leverages its built-in concurrency features.

## Tests

Unit tests are included in the `tests/` directory. They use mocks to ensure deterministic and offline execution.
