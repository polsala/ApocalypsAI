# Go Concurrent Fetcher

This utility allows you to fetch multiple URLs concurrently and get a summary of their status (success, failure, or timeout).

## Features

*   Concurrent fetching of URLs using Go routines.
*   Configurable timeout for each request.
*   Clear reporting of results.

## Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run the utility:**
    Provide a list of URLs as command-line arguments.

    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com http://invalid.url https://httpbin.org/delay/5
    ```

    You can also specify a timeout (in seconds) using the `-timeout` flag:

    ```bash
    ./concurrent-fetcher -timeout 3 https://www.google.com https://www.github.com http://invalid.url https://httpbin.org/delay/5
    ```

## Example Output

```
Fetching URLs with a timeout of 10 seconds...

Results:
----------------------------------------
URL: https://www.google.com
Status: Success
Time: 150ms
----------------------------------------
URL: https://www.github.com
Status: Success
Time: 220ms
----------------------------------------
URL: http://invalid.url
Status: Error (Get "http://invalid.url": dial tcp: lookup invalid.url: no such host)
Time: 50ms
----------------------------------------
URL: https://httpbin.org/delay/5
Status: Timeout (context deadline exceeded)
Time: 5s
----------------------------------------

Summary:
Successful: 2
Errors: 1
Timeouts: 1
```

## Development

This utility is written in Go. To run tests, navigate to the `src` directory and run `go test`.
