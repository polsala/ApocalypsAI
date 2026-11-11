## Nightly Go Concurrent Fetcher

This utility is a standalone Go program designed to fetch multiple URLs concurrently and report their HTTP status codes. It's useful for quickly checking the health of a list of web resources.

### Usage

1.  **Build the Go program:**
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run the program:**
    The program expects URLs to be provided as command-line arguments.
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://nonexistent.example.com
    ```

### Output

The output will list each URL along with its HTTP status code or an error message if the fetch failed.

```
URL: https://www.google.com, Status: 200 OK
URL: https://www.github.com, Status: 200 OK
URL: https://nonexistent.example.com, Error: Get "https://nonexistent.example.com": dial tcp: lookup nonexistent.example.com: no such host
```

### Features

*   **Concurrency:** Utilizes Go's goroutines to fetch URLs in parallel, significantly speeding up the process.
*   **Error Handling:** Gracefully handles network errors and non-2xx HTTP responses.
*   **Simple CLI:** Easy to use with command-line arguments.

### Testing

Automated tests are included to verify the functionality. Run them using:

```bash
go test ./...
```
