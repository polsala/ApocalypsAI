# nightly-voidsync-broadcaster

A lightweight concurrent UDP multicast message broadcaster written in Go. Designed for ephemeral inter-service communication in distributed systems.

## Features

- Concurrent broadcasting
- UDP multicast support
- CLI interface
- Zero dependencies

## Usage

```bash
# Send a message to the multicast group
./voidsync-broadcaster -message="Hello, wasteland!" -group="224.0.0.1:9999"

# Listen for messages
./voidsync-broadcaster -listen -group="224.0.0.1:9999"
```

## Build

```bash
go build -o voidsync-broadcaster src/main.go
```

## Test

```bash
go test -v ./tests
```
