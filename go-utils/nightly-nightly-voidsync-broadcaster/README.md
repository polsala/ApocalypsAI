# nightly-voidsync-broadcaster

A lightweight concurrent UDP multicast broadcaster written in Go. Designed for ephemeral service-to-service announcements in distributed systems.

## Features
- Concurrent broadcasting with timeouts
- Lightweight and dependency-free
- CLI interface with configurable multicast address and port

## Usage

```bash
# Send a message to the multicast group
./voidsync-broadcaster -message="System reboot in 5 minutes" -group="224.0.0.1:9999"
```

## Build

```bash
go build -o voidsync-broadcaster src/main.go
```

## Test

```bash
go test -v ./tests
```
