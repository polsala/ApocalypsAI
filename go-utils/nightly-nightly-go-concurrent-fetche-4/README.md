## Nightly Go Concurrent Fetcher

A whimsical yet useful Go utility designed to fetch multiple URLs concurrently. It's perfect for quickly checking the status of a list of web resources, whether they're vital survival caches or just your favorite apocalyptic news feeds.

### Philosophy

Inspired by the need for speed and efficiency in a chaotic world, this tool leverages Go's concurrency primitives to get the job done without waiting around.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent-fetcher main.go
    ```

2.  **Run with a list of URLs:**
    Provide URLs as command-line arguments. For example:
    ```bash
    ./concurrent-fetcher https://example.com http://nonexistent.invalid https://google.com
    ```

### Output

The utility will print the status of each URL, indicating whether it was fetched successfully or encountered an error. Successful fetches will show the HTTP status code.

### Example Output:

```
Fetching https://example.com...
  -> Success: 200 OK
Fetching http://nonexistent.invalid...
  -> Error: Get "http://nonexistent.invalid": dial tcp: lookup nonexistent.invalid: no such host
Fetching https://google.com...
  -> Success: 200 OK
```

### Contributing

Feel free to fork this repository and add more features, such as timeout configurations, retry mechanisms, or different output formats. Just remember to follow the ApocalypsAI philosophy: anarchy with discipline!
