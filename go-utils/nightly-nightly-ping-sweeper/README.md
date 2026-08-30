# nightly-ping-sweeper

A whimsical concurrent network utility that pings a list of hosts to see which are still alive in the post‑apocalyptic wasteland.

## Usage

```sh
# Run directly with go (no build step required)
go run ./src/main.go host1.com host2.com
```

or build a binary:

```sh
go build -o nightly-ping-sweeper ./src/main.go
./nightly-ping-sweeper host1.com host2.com
```

## How it works

- Uses Go's goroutines to ping all hosts in parallel.
- Attempts a TCP connection on port **80** with a **2‑second** timeout.
- Prints a cheerful emoji‑filled status line for each host.

## Testing

```sh
go test ./...
```
