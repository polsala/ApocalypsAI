# Go Concurrent Fetcher

This utility fetches multiple URLs concurrently using Go's goroutines and channels. It reports the status code and response time for each URL.

## Features

*   Concurrent fetching of multiple URLs.
*   Reports HTTP status codes.
*   Measures and reports response times.
*   Handles basic network errors gracefully.

## Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run the utility with a list of URLs:**
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://www.example.com
    ```

    You can also pipe URLs from standard input:
    ```bash
    echo "https://www.google.com\nhttps://www.github.com" | ./concurrent-fetcher
    ```

## Testing

Run the tests using Go's testing framework:

```bash
    go test ./...
    ```
