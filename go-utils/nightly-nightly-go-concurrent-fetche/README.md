# Go Concurrent Fetcher

This utility allows you to fetch multiple URLs concurrently and get a summary of their status (HTTP status code, response time, and any errors).

## Features

*   **Concurrency**: Utilizes Go's goroutines to fetch URLs in parallel.
*   **Error Handling**: Reports any errors encountered during fetching.
*   **Performance Metrics**: Records response time for each URL.
*   **Clear Output**: Presents results in a human-readable format.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run with a list of URLs**: 
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://invalid.url.xyz
    ```

## Example Output

```
Fetching URLs concurrently...

Results:
--------------------------------------------------
URL: https://www.google.com
Status: 200 OK
Response Time: 150ms
Error: <nil>
--------------------------------------------------
URL: https://www.github.com
Status: 200 OK
Response Time: 300ms
Error: <nil>
--------------------------------------------------
URL: https://invalid.url.xyz
Status: 0 
Response Time: 500ms
Error: Get "https://invalid.url.xyz": dial tcp: lookup invalid.url.xyz: no such host
--------------------------------------------------
```
