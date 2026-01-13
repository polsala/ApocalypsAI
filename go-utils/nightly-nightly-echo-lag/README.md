# nightly-echo-lag

A whimsical concurrent CLI that fetches HTTP headers from a list of URLs and echoes playful status messages.

## Usage

```bash
go run src/main.go https://example.com https://golang.org
```

The program will perform HEAD requests concurrently and print each URL with its HTTP status code and a fun message.

## Features

- Concurrent HTTP HEAD requests
- Timeout handling (5 seconds per request)
- Whimsical status messages based on HTTP status codes
- Simple command-line interface

## Installation

```bash
go install github.com/polsala/ApocalypsAI/utils/nightly-echo-lag@latest
```

## Testing

Run the tests with:

```bash
go test ./...
```
