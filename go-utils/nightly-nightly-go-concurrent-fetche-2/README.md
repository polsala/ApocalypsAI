## Nightly Go Concurrent Fetcher

This utility, built with Go, allows you to concurrently fetch multiple URLs and report their HTTP status codes and response times. It's designed to be a simple yet effective tool for checking the health of a list of web resources.

### Features

*   **Concurrency**: Utilizes Go's goroutines to fetch URLs in parallel.
*   **Status Reporting**: Displays the HTTP status code for each URL.
*   **Response Time Measurement**: Records and displays the time taken to receive a response.
*   **Error Handling**: Gracefully handles network errors and timeouts.

### Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run with a list of URLs**: 
    You can provide URLs as command-line arguments.
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://httpbin.org/delay/2
    ```

    Alternatively, you can pipe a list of URLs to the utility:
    ```bash
    echo "https://www.google.com\nhttps://www.github.com" | ./concurrent-fetcher
    ```

### Configuration

*   **Timeout**: The default timeout for each request is 10 seconds. This can be adjusted in the `main.go` file.

### Testing

To run the included tests:

```bash
go test ./...
```

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
