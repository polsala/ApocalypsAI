# nightly-emoji-echo-server

A whimsical yet useful Go utility that runs a TCP echo server. Every line received from a client is sent back with a randomly chosen emoji appended.

## Features

- Handles multiple clients concurrently using goroutines.
- Deterministic random emoji selection (seeded by `SEED` env var for testing, otherwise time‑based).
- Zero external dependencies – pure Go standard library.

## Build

```bash
# Clone the repository (or copy the utility folder) and build
cd go-utils/nightly-emoji-echo-server
go build -o emoji-echo-server ./src/main.go
```

## Run

```bash
# Default listens on port 8080
./emoji-echo-server

# Custom port via PORT env var
PORT=9090 ./emoji-echo-server
```

## Example

```bash
$ nc localhost 8080
Hello world!
Hello world! 😎
```

## Testing

```bash
go test ./tests
```

The test suite starts the server on a random free port, sends a line, and verifies the echoed response contains one of the expected emojis.
