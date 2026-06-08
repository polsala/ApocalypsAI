# Go Concurrent Fetcher

This utility allows you to fetch multiple URLs concurrently using Go's goroutines and channels. It's designed to be a simple yet powerful tool for checking the availability and response times of various web resources.

## Features

*   **Concurrent Fetching**: Utilizes goroutines to fetch multiple URLs simultaneously, significantly speeding up the process.
*   **Error Handling**: Reports any errors encountered during the fetching process.
*   **Response Time**: Measures and reports the time taken to receive a response from each URL.
*   **Status Reporting**: Clearly indicates whether a URL was fetched successfully or if an error occurred.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run with a list of URLs**: 
    The utility expects URLs to be provided as command-line arguments.
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://invalid.url.com
    ```

## Example Output

```
Fetching: https://www.google.com
  Status: OK
  Time: 150ms
Fetching: https://www.github.com
  Status: OK
  Time: 300ms
Fetching: https://invalid.url.com
  Status: Error
  Error: Get "https://invalid.url.com": dial tcp: lookup invalid.url.com: no such host
```

## Development

This utility is written in Go and leverages its concurrency primitives.

*   **`main.go`**: Contains the main application logic, including argument parsing and goroutine management.
*   **`fetcher.go`**: Implements the core fetching logic for a single URL.
*   **`tests/`**: Contains unit tests for the fetching logic.
