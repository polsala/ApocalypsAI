# Nightly Portal Port Echo

A whimsical concurrent port scanner written in Go. It scans a range of TCP ports on a host and announces any open ports with a portal‑themed message.

## Installation

```sh
go build -o portal-echo ./src/main.go
```

## Usage

```sh
./portal-echo -host localhost -start 8000 -end 8100 -c 100
```

**Options**
- `-host` target hostname or IP (default "localhost")
- `-start` starting port (inclusive)
- `-end` ending port (inclusive)
- `-c` concurrency level (default 100)

## Example Output

```
🌀 Port 8080 is open! The portal hums.
🌀 Port 8090 is open! The portal hums.
```

## Testing

Run the deterministic test suite with:

```sh
go test ./...
```
