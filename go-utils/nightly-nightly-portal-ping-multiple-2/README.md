# Portal Ping Multiplexer

A whimsical concurrent HTTP ping tool that probes multiple endpoints and reports latency statistics, as if opening portals to other dimensions.

## Features

- Accepts URLs via command‑line arguments or stdin
- Sends requests concurrently
- Shows per‑endpoint success/failure with latency
- Summarises overall success rate and average latency
- Configurable request timeout

## Installation

```sh
go build -o portal-ping ./src/main.go
```

## Usage

```sh
# Ping a list of URLs
./portal-ping https://example.com https://golang.org

# Or pipe a list
cat urls.txt | ./portal-ping
```

## Options

- `-timeout duration` – request timeout (default 5s)

## Testing

```sh
go test ./tests/...
```
