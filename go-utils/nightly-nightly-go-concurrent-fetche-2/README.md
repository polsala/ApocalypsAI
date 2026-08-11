# Go Concurrent Fetcher

This utility allows you to fetch multiple URLs concurrently using Go's powerful goroutines and channels. It's designed to be a simple yet effective tool for checking the status of a list of web resources.

## Features

*   **Concurrency**: Fetches URLs in parallel for faster results.
*   **Status Reporting**: Reports the HTTP status code and response time for each URL.
*   **Error Handling**: Gracefully handles network errors and timeouts.
*   **Configurable Timeout**: Allows setting a global timeout for all requests.

## Usage

1.  **Build the project**: 
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run the utility**: 
    The utility expects a list of URLs as command-line arguments. You can also specify a timeout duration (e.g., `5s`, `1m`).

    **Example with URLs only**: 
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://www.example.com
    ```

    **Example with timeout**: 
    ```bash
    ./concurrent-fetcher --timeout 10s https://www.google.com https://www.github.com https://www.example.com
    ```

    **Example with a mix of valid and invalid URLs**: 
    ```bash
    ./concurrent-fetcher https://httpbin.org/status/200 https://httpbin.org/status/404 https://nonexistent.domain.invalid
    ```

## Output Format

The output will be a list of results, each containing:

*   **URL**: The URL that was fetched.
*   **Status Code**: The HTTP status code received (e.g., 200, 404, 0 for errors).
*   **Response Time**: The time taken to receive the response in milliseconds.
*   **Error**: Any error encountered during the fetch (e.g., connection refused, DNS lookup failed).

## Development

This utility is written in Go and leverages standard library packages for HTTP requests and concurrency.

## Testing

Automated tests are included to verify the functionality. These tests use mocks to simulate network responses without requiring actual network access.

To run tests:

```bash
    go test ./...
    ```
