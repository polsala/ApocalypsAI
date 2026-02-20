# nightly-qr-encoder
A whimsical Go CLI that encodes text into an ASCII QR‑like pattern using concurrent goroutines.

## Installation
```sh
go build -o qr-encoder ./src/main.go
```

## Usage
```sh
echo "HELLO" | ./qr-encoder
```
or
```sh
./qr-encoder "HELLO"
```

## How it works
Each character is processed in its own goroutine, converting the rune value to a line of "#" and space characters based on its binary representation.
