# nightly-void-echo-server

A whimsical concurrent TCP echo server written in Go. It echoes back any message you send it, but with a twist: it returns the message in reverse! It also keeps track of active connections and total messages processed.

## Features

- Concurrent handling of multiple clients
- Message reversal for fun responses
- Tracks active connections and message counts
- Graceful shutdown on SIGINT/SIGTERM

## Usage

1. Start the server:

```bash
go run src/main.go
```

2. Connect using telnet or nc:

```bash
telnet localhost 8080
# or
nc localhost 8080
```

3. Type a message and see it echoed back in reverse.

## Example

Client sends: `hello`

Server responds: `olleh`
