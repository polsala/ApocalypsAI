# Go Concurrent Fetcher

This utility, built with Go, allows you to fetch data from a list of URLs concurrently. It's designed to be efficient and provide clear feedback on which URLs succeeded and which failed.

## Features

*   **Concurrency**: Utilizes Go's goroutines to fetch multiple URLs simultaneously.
*   **Error Handling**: Reports any errors encountered during fetching.
*   **Progress Indication**: Shows which URLs are being processed.
*   **Results Summary**: Provides a clear summary of successful and failed fetches.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent_fetcher .
    ```

2.  **Run the utility**: 
    The utility expects a list of URLs as command-line arguments.
    ```bash
    ./concurrent_fetcher https://example.com http://nonexistent.invalid https://google.com
    ```

## Example Output

```
Processing URL: https://example.com
Processing URL: http://nonexistent.invalid
Processing URL: https://google.com

Successes:
- https://example.com (Status: 200 OK)
- https://google.com (Status: 200 OK)

Failures:
- http://nonexistent.invalid (Error: Get "http://nonexistent.invalid": dial tcp: lookup nonexistent.invalid: no such host)
```

## Development

This utility is written in Go and leverages its built-in concurrency primitives.

## Tests

Unit tests are included to verify the functionality of the fetcher logic. They use mocks to simulate network responses without making actual HTTP requests.

To run tests:
```bash
go test ./...
```
