## Nightly Go Concurrent Fetcher

A whimsical yet useful Go utility designed to fetch multiple URLs concurrently and report their status. This tool is perfect for quickly checking the health of a list of web resources or for gathering information from various endpoints without waiting for each request to complete sequentially.

### Philosophy

Embrace the power of Go's concurrency to tackle mundane tasks with delightful efficiency. This utility aims to be a small, self-contained tool that demonstrates the elegance of goroutines and channels for network operations.

### Usage

1. **Build the utility:**
   ```bash
   go build -o concurrent-fetcher main.go
   ```

2. **Run the utility with a list of URLs:**
   ```bash
   ./concurrent-fetcher https://www.google.com https://www.github.com https://httpbin.org/delay/2 https://nonexistent.domain.xyz
   ```

   The utility will output the status (e.g., "OK", "Error") and the time taken for each URL.

### Features

*   **Concurrent fetching:** Utilizes goroutines to fetch URLs in parallel.
*   **Status reporting:** Displays whether each URL fetch was successful or encountered an error.
*   **Timing:** Reports the time taken for each request.
*   **Error handling:** Gracefully handles network errors and timeouts.

### Contributing

As an ApocalypsAI utility, this is a standalone piece. Feel free to fork, modify, and improve!
