# Go Concurrent Fetcher

This utility allows you to fetch multiple URLs concurrently and get a summary of their status (success, failure, status code, and duration).

## Features

*   **Concurrency**: Utilizes Go's goroutines to fetch URLs in parallel.
*   **Error Handling**: Reports failed fetches with error messages.
*   **Performance Metrics**: Records the time taken for each fetch.
*   **Configurable**: Easily add or remove URLs from the input list.

## Usage

1.  **Build the utility**: 
    ```bash
    go build -o concurrent-fetcher .
    ```

2.  **Run the utility**: 
    ```bash
    ./concurrent-fetcher
    ```

    The utility will fetch the predefined list of URLs and print the results to the console.

## Example Output

```
Fetching URLs concurrently...

URL: https://www.google.com
  Status: Success (200 OK)
  Duration: 150ms

URL: https://httpbin.org/delay/2
  Status: Success (200 OK)
  Duration: 2.1s

URL: https://nonexistent.domain.xyz
  Status: Failed (Get "https://nonexistent.domain.xyz": dial tcp: lookup nonexistent.domain.xyz: no such host)
  Duration: 50ms

Summary:
  Total URLs: 3
  Successful: 2
  Failed: 1
```

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
