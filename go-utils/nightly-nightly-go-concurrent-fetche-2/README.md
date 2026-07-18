# Go Concurrent Fetcher

This utility, built with Go, allows you to concurrently fetch multiple URLs and report their HTTP status codes and response times. It's designed to be a simple yet effective tool for checking the health of a list of web resources.

## Features

*   **Concurrency**: Utilizes Go's goroutines to fetch URLs in parallel.
*   **Status Reporting**: Displays the HTTP status code for each URL.
*   **Response Time Measurement**: Records and displays the time taken to receive a response.
*   **Error Handling**: Gracefully handles network errors and non-2xx status codes.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent_fetcher .
    ```

2.  **Run with a list of URLs**: 
    You can provide URLs as command-line arguments or pipe them from standard input.

    **Command-line arguments**: 
    ```bash
    ./concurrent_fetcher https://www.google.com https://www.github.com https://invalid.url
    ```

    **Piping from stdin**: 
    ```bash
    echo "https://www.example.com\nhttps://httpbin.org/delay/2" | ./concurrent_fetcher
    ```

## Output Format

The output will be a list of lines, each representing a fetched URL, its status code, and the time taken:

```
URL: https://www.google.com, Status: 200 OK, Time: 150ms
URL: https://www.github.com, Status: 200 OK, Time: 300ms
URL: https://invalid.url, Status: Error (Get "https://invalid.url": dial tcp: lookup invalid.url: no such host), Time: 50ms
```

## Testing

Automated tests are included to verify the functionality. Run them using:

```bash
go test ./...
```
