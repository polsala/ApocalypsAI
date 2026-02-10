# nightly-echo-ping-pong

A tiny Go utility that can act as a **UDP ping‑pong server** or **client**.  The server listens for messages that start with `ping:` and replies with `pong:` followed by the original payload.  The client sends a configurable number of ping messages and prints the received pong replies.

## Why?
* Quick way to verify UDP connectivity between two hosts.
* Fun, whimsical demonstration of Go's concurrency primitives.
* No external dependencies – just the Go standard library.

## Build
```bash
# From the repository root
cd utils/go-utils/nightly-echo-ping-pong
go build -o pingpong ./src/main.go
```

## Usage
### Server mode
```bash
./pingpong -mode=server -port=9000
```
The server will run indefinitely, replying to any `ping:` messages it receives.

### Client mode
```bash
./pingpong -mode=client -host=127.0.0.1 -port=9000 -count=5
```
The client sends `count` ping messages (`ping:0` … `ping:4`) and prints each pong response.

## Testing
```bash
go test ./tests
```
All tests are deterministic and do not require actual network access.
