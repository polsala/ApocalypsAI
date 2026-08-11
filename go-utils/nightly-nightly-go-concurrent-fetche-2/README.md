## Nightly Go Concurrent Fetcher

A whimsical yet useful Go utility designed to fetch data concurrently from a list of URLs. It provides a clear overview of successful and failed requests, making it handy for checking the health of multiple endpoints or gathering data efficiently.

### Philosophy

Embrace the power of Go's concurrency to tackle mundane tasks with flair. This utility aims to be a simple, robust tool for anyone needing to monitor or interact with multiple web resources simultaneously.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent_fetcher .
    ```

2.  **Run with a list of URLs:**
    The utility expects URLs to be provided as command-line arguments. If no arguments are provided, it will use a default set of example URLs.

    ```bash
    ./concurrent_fetcher https://example.com http://httpbin.org/delay/1 https://nonexistent.domain
    ```

### Output

The utility will print a summary of the fetch operations, including:

*   Total URLs processed
*   Number of successful fetches
*   Number of failed fetches
*   A list of URLs that failed to fetch, along with their error messages.

### Example Output:

```
Processing 3 URLs...

--- Fetch Summary ---
Total URLs: 3
Successful: 2
Failed: 1

--- Failed URLs ---
- https://nonexistent.domain: Get "http://nonexistent.domain": dial tcp: lookup nonexistent.domain: no such host
```

### Contributing

Feel free to fork this repository and submit pull requests for improvements or new features. All contributions are welcome!
