## Nightly Go Concurrent Fetcher

A whimsical yet useful Go utility designed to fetch multiple URLs concurrently and report their status. This tool is perfect for quickly checking the health of a list of web endpoints or gathering basic information from them without overwhelming your system.

### Philosophy

Embrace the power of Go's concurrency to perform network operations efficiently. This utility aims to be a simple, standalone tool that can be easily integrated into various workflows.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run the utility with a list of URLs:**
    The utility expects URLs to be provided as command-line arguments.

    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://httpbin.org/delay/3 https://nonexistent.domain.xyz
    ```

### Output

The utility will print the status of each URL, including its status code (if available) and the time taken to fetch it. Errors will be clearly indicated.

Example Output:

```
[INFO] Fetching: https://www.google.com
[INFO] Fetching: https://www.github.com
[INFO] Fetching: https://httpbin.org/delay/3
[INFO] Fetching: https://nonexistent.domain.xyz
[SUCCESS] https://www.google.com - Status: 200 OK - Time: 150ms
[SUCCESS] https://www.github.com - Status: 200 OK - Time: 220ms
[ERROR] https://nonexistent.domain.xyz - Error: Get "https://nonexistent.domain.xyz": dial tcp: lookup nonexistent.domain.xyz: no such host
[SUCCESS] https://httpbin.org/delay/3 - Status: 200 OK - Time: 3100ms
```

### Contributing

Feel free to fork this repository and submit pull requests. All contributions are welcome!
