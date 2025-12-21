# nightly-url-status-reporter

A whimsical yet useful Go utility that concurrently checks the HTTP status of a list of URLs and reports the results in JSON. Perfect for quick sanity checks of web services, APIs, or just to see which sites are alive.

## Features

- Concurrent HTTP HEAD requests for speed.
- Simple CLI: `-urls` comma‑separated list or `-file` path to a file with one URL per line.
- Outputs a JSON map of URL → status code.
- Handles errors gracefully and reports them.

## Usage

```bash
# Check a few URLs
go run src/main.go -urls https://example.com,https://google.com

# Or from a file
go run src/main.go -file urls.txt
```

## Example Output

```json
{
  "https://example.com": 200,
  "https://google.com": 200,
  "https://nonexistent.xyz": 0
}
```

## Building

```bash
go build -o urlstatus src/main.go
```

## Testing

Run the test suite:

```bash
go test ./tests
```

Enjoy the status parade!
