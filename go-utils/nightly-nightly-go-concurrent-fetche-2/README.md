## nightly-go-concurrent-fetcher

A whimsical yet useful Go utility designed to fetch data concurrently from a list of URLs. It reports the success and failure rates of these fetches, providing a quick overview of the health of a set of web resources.

### Philosophy

Inspired by the need for quick, reliable checks in a chaotic world, this tool uses Go's powerful concurrency features to efficiently probe multiple endpoints. It's designed to be simple to use and understand, even for those new to Go.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run with a list of URLs:**
    The utility expects URLs to be provided as command-line arguments.
    ```bash
    ./concurrent-fetcher https://example.com http://nonexistent.invalid https://google.com
    ```

### Output

The utility will print a summary of the fetch operations, including:

*   Total URLs processed
*   Number of successful fetches
*   Number of failed fetches
*   Success rate
*   Failure rate

It will also list any URLs that failed to fetch.

### Example Output

```
--- Concurrent Fetcher Report ---
Total URLs: 3
Successful Fetches: 2
Failed Fetches: 1
Success Rate: 66.67%
Failure Rate: 33.33%

Failed URLs:
- http://nonexistent.invalid
-------------------------------
```

### Contributing

This is a standalone utility. Contributions are welcome via pull requests to the ApocalypsAI repository.

### License

[MIT License](LICENSE)
