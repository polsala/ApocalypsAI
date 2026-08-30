# nightly-echo-multiplier

A whimsical concurrent TCP echo server written in Go. It echoes each line received from a client, appending a random emoji for a touch of fun. Designed to showcase Go's concurrency primitives while being a handy tool for quick network testing.

## Features

- Handles multiple clients concurrently.
- Appends a deterministic random emoji (seeded for reproducibility in tests).
- Configurable listen address via `-addr` flag (default `:8080`).

## Build & Run

```sh
go build -o echo-multiplier ./src
./echo-multiplier -addr :8080
```

## Example

```sh
$ nc localhost 8080
hello
hello 🌟
```

## Testing

```sh
go test ./tests
```
