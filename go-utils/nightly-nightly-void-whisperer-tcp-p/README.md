# nightly-void-whisperer-tcp-proxy

A concurrent TCP proxy written in Go that forwards traffic between clients and servers with optional whimsical logging.

## Features

- Concurrent connection handling
- Configurable target host and port
- Toggleable verbose/whimsical logging
- Graceful shutdown on interrupt signal

## Usage

```bash
go run src/main.go --listen :8080 --target example.com:80 [--verbose]
```

## Example

Forward local port 9090 to httpbin.org:80:

```bash
go run src/main.go --listen :9090 --target httpbin.org:80
```

## Testing

Run included tests with:

```bash
go test -v ./tests
```
