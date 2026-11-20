# Apocalypse Echo Bot

A whimsical concurrent TCP echo server written in Go. It listens for incoming connections and echoes back each line prefixed with an apocalypse‑themed tag (e.g., `[Doom]`). Perfect for testing network tools or adding a bit of drama to your dev environment.

## Build

```sh
go build -o echo-bot ./src
```

## Run as server

```sh
./echo-bot -listen :8080
```

## Run as client

```sh
./echo-bot -client localhost:8080
```

## How it works

- The server accepts multiple connections concurrently using goroutines.
- Each incoming line is read, prefixed with a tag from a rotating list, and sent back.
- The client mode reads stdin, sends each line, and prints the server response.

## Testing

```sh
go test ./...
```
