# Apocalyptic Echo Server

A whimsical concurrent TCP echo server written in Go. It prefixes each incoming line with a random apocalypse‑themed phrase (e.g., "The skies burn:", "Dust storms whisper:").

## Usage

```sh
go run ./src/main.go -port 8080
```

Connect with netcat:

```sh
nc localhost 8080
Hello
# Output: The skies burn: Hello
```

## How it works

- Listens on a configurable port.
- For each client, spawns a goroutine.
- Reads lines, prefixes with a random phrase, sends back.
- Uses a seeded random source for reproducibility in tests.

## Testing

```sh
go test ./...
```
