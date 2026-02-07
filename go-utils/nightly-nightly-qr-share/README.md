# nightly-qr-share

A whimsical Go utility that spins up a temporary HTTP server to share a QR code of any text. Perfect for quick, on‑the‑fly sharing of URLs, Wi‑Fi passwords, or secret messages. The server auto‑shuts down after a configurable timeout.

## Installation

```sh
go build -o nightly-qr-share ./src
```

## Usage

```sh
./nightly-qr-share -text "https://example.com" -port 8080 -ttl 300
```

- `-text` : The string to encode into a QR code.
- `-port` : Port for the HTTP server (default 8080).
- `-ttl`  : Time‑to‑live in seconds before the server stops (default 300).

Open `http://localhost:8080/qr.png` in a browser to see the QR code.

## How it works

The program uses the `github.com/skip2/go-qrcode` library to generate a PNG image in memory and serves it via a simple `net/http` handler. A background goroutine stops the server after the TTL expires.
