# nightly-portal-ping

A whimsical concurrent port scanner that checks a range of ports on a host and reports open ports with sparkle. Built in Go, leveraging goroutines for speed.

## Usage

```sh
go run ./src/main.go -host example.com -start 1 -end 1024 -concurrency 100
```

Outputs lines like:

```
✨ Port 80 is open! ✨
```

## Build

```sh
go build -o portal-ping ./src/main.go
```

## Flags

- `-host` (string, required): target hostname or IP.
- `-start` (int, default 1): starting port.
- `-end` (int, default 1024): ending port (inclusive).
- `-concurrency` (int, default 100): number of concurrent workers.

## Testing

```sh
go test ./tests
```
