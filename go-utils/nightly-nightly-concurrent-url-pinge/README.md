# nightly-concurrent-url-pinger

A whimsical Go CLI that concurrently pings a list of URLs and reports whether each is reachable. Useful for quick health checks of services in a post‑apocalyptic network.

## Usage

```sh
# Pass URLs as arguments
go run ./src/main.go https://example.com https://nonexistent.invalid
```

Or pipe a list of URLs (one per line) via stdin:

```sh
cat urls.txt | go run ./src/main.go
```

## Build

```sh
go build -o urlpinger ./src/main.go
```

## Options

- `-c N` : maximum concurrent requests (default 5)

The tool prints each URL followed by `UP` or `DOWN`.
