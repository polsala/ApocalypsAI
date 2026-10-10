# Nightly Network Pulse

A whimsical yet practical concurrent HTTP latency checker.  Give it a list of URLs and it will ping them in parallel, then output a JSON array with each URL's status code, response time (ms), and any error.

## Build

```sh
go build -o network-pulse ./src/main.go
```

## Usage

```sh
./network-pulse -timeout 3 https://example.com https://golang.org
```

* `-timeout` – request timeout in seconds (default 5)

The program prints a pretty‑printed JSON summary to stdout.

## Example Output

```json
[
  {
    "url": "https://example.com",
    "status_code": 200,
    "duration_ms": 123.4
  },
  {
    "url": "https://nonexistent.invalid",
    "error": "dial tcp: lookup nonexistent.invalid: no such host"
  }
]
```

## Testing

```sh
go test ./tests/...
```
