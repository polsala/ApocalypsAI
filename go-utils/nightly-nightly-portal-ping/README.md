# nightly-portal-ping

A whimsical concurrent ping utility that checks the latency to multiple hosts and reports them as "portal opening times". Useful for quick network diagnostics with a dash of apocalypse flair.

## Installation

```sh
go build -o portal-ping ./src/main.go
```

## Usage

```sh
./portal-ping host1.com example.org 192.0.2.1
```

Outputs:

```
🔮 Portal to host1.com opened in 23ms
🔮 Portal to example.org opened in 45ms
❌ Failed to open portal to 192.0.2.1: timeout
```

## How it works

- Uses Go's goroutines to ping all hosts concurrently.
- Measures TCP connection latency to port 80 (configurable via `-port` flag).
- Reports results in a whimsical format.

## Testing

Run `go test ./...` to execute deterministic unit tests that mock network calls.
