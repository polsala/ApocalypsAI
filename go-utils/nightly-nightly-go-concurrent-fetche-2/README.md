## Nightly Go Concurrent Fetcher

This utility, built with Go, allows you to concurrently fetch multiple URLs and report their status (HTTP status code and response time). It's designed for quick checks of web service availability and performance.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent-fetcher main.go
    ```

2.  **Run the utility:**
    Provide a list of URLs as command-line arguments.
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://httpbin.org/delay/2
    ```

### Features

*   **Concurrency:** Utilizes Go's goroutines to fetch multiple URLs simultaneously.
*   **Error Handling:** Reports any errors encountered during fetching.
*   **Response Time:** Measures and reports the time taken to receive a response from each URL.
*   **HTTP Status Code:** Displays the HTTP status code for each successful request.

### Example Output

```
URL: https://www.google.com
  Status: 200 OK
  Response Time: 150ms

URL: https://www.github.com
  Status: 200 OK
  Response Time: 300ms

URL: https://httpbin.org/delay/2
  Status: 200 OK
  Response Time: 2.15s

URL: https://nonexistent.example.com
  Error: Get "https://nonexistent.example.com": dial tcp: lookup nonexistent.example.com: no such host
```
