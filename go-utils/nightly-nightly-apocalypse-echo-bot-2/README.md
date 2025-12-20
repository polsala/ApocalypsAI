# nightly-apocalypse-echo-bot

A whimsical concurrent Go TCP echo server that prepends a random apocalypse-themed phrase to each line received. Useful for testing network clients and adding fun to dev environments.

## Usage

```sh
go run src/main.go
```

The server listens on port 4000 by default. You can specify a different port:

```sh
go run src/main.go -port 12345
```

Connect with netcat:

```sh
nc localhost 4000
Hello
#=> [The Skies Crack] Hello
```

## How it works

- Listens for TCP connections.
- For each connection, spawns a goroutine.
- Reads lines, prepends a deterministic random phrase (seeded for reproducibility).
- Writes back the transformed line.

## Testing

```sh
go test ./...
```
