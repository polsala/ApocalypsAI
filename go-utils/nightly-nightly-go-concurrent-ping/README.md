# nightly-go-concurrent-ping

Utility that concurrently pings a list of URLs and reports their HTTP status. Useful for quick health checks.

## Usage

```sh
go run ./src/main.go -file urls.txt -concurrency 5
```

`urls.txt` contains one URL per line.

## Options

- `-file` path to file with URLs (required)
- `-concurrency` max concurrent requests (default 10)

## Output

Each line: `<url> -> <status>` where status is HTTP status code or error.
