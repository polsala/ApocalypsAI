# nightly-remote-echo-bot

A whimsical concurrent Go TCP echo server that appends an apocalypse‑themed suffix to each line. Useful for testing network clients and adding fun to dev environments.

## Usage

```sh
go run src/main.go -port 4000
```

Send a line:

```sh
echo "Hello" | nc localhost 4000
```

Response (example):

```
Hello [The world crumbles]
```

## Flags

- `-port` (default 4000): TCP port to listen on.
- `-testmode` (default false): When true, uses a deterministic suffix `[Apocalypse]` for testing.

## Testing

```sh
go test ./...
```
