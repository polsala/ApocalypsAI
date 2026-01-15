# nightly-apocalypse-echo-bot

A whimsical concurrent TCP echo service that repeats your messages with an apocalypse‑themed prefix. Useful for quick network testing or a bit of fun chat between terminals.

## Usage

### Server

```sh
go run src/main.go -mode=server -port=8080
```

The server listens on the given port and echoes each line prefixed with `⚡️[Apocalypse] `.

### Client

```sh
go run src/main.go -mode=client -port=8080 -msg="Hello world"
```

The client sends the message and prints the server's response.

## Tests

```sh
go test ./...
```
