# Hopeful UDP Relay

A lightweight concurrent UDP relay written in Go. Listens on a UDP address and forwards any received packets to a broadcast address. Perfect for whimsical post‑apocalyptic message passing.

## Build

```sh
go build -o udp-relay ./src
```

## Usage

```sh
./udp-relay -listen :9000 -broadcast 239.0.0.1:9000
```

- `-listen`   UDP address to listen on (e.g., `:9000` or `127.0.0.1:9000`).
- `-broadcast` UDP address to forward packets to.

## How it works

The program creates two UDP sockets. One receives packets, the other sends them to the broadcast address. Each packet is handled in its own goroutine, allowing high concurrency.

## Testing

```sh
go test ./...
```
