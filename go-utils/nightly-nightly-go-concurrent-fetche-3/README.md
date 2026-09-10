# Go Concurrent Fetcher

This utility allows you to fetch multiple URLs concurrently and get a summary of their status (success, failure, or error).

## Features

*   Concurrent fetching of URLs using Go routines.
*   Reports status for each URL (HTTP status code or error message).
*   Configurable timeout for requests.

## Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run with a list of URLs:**
    ```bash
    ./concurrent-fetcher https://www.google.com https://www.github.com https://invalid.url.xyz
    ```

    You can also specify a timeout (in seconds) using the `-timeout` flag:
    ```bash
    ./concurrent-fetcher -timeout 5 https://www.google.com https://www.github.com
    ```

## Example Output

```
URL: https://www.google.com
  Status: 200 OK
URL: https://www.github.com
  Status: 200 OK
URL: https://invalid.url.xyz
  Error: Get "https://invalid.url.xyz": dial tcp: lookup invalid.url.xyz: no such host
```
