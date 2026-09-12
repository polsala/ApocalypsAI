# nightly-qr-encoder

A whimsical Go CLI that converts input strings into ASCII QR‑code‑like art. It reads lines from stdin (or a file) and prints a stylized QR representation for each line, processing them concurrently.

## Installation

```sh
go build -o nightly-qr-encoder ./src/main.go
```

## Usage

```sh
# Encode a single line
echo "Hello, world!" | ./nightly-qr-encoder

# Encode a file with multiple lines
./nightly-qr-encoder -file messages.txt
```

## How it works

The tool spawns a goroutine per input line, uses a deterministic placeholder algorithm to generate a pseudo‑QR pattern, and prints results as soon as they are ready.

## Testing

```sh
go test ./...
```
