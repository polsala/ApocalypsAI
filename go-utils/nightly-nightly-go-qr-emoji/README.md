# nightly-go-qr-emoji

**Generate QR codes rendered as emoji art**

This utility is a tiny Go command‑line tool that takes an arbitrary string and prints a QR code made of black and white square emojis (⬛️ and ⬜️).  It is perfect for sharing short links or secrets in a terminal‑friendly, whimsical way.

## Installation

```bash
# Clone the repository (or copy the generated files into your own repo)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-go-qr-emoji

# Build the binary (requires Go 1.22+)
go build -o qr-emoji ./src/main.go
```

You can also install it directly with `go install`:

```bash
go install github.com/polsala/nightly-go-qr-emoji/src@latest
```

## Usage

```bash
./qr-emoji "https://example.com"
```

The program will output something like:

```
⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️
⬛️⬜️⬜️⬜️⬜️⬜️⬜️⬛️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬛️
... (more rows) ...
⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️
```

Each line corresponds to a row of the QR matrix; black squares are rendered as `⬛️` and white squares as `⬜️`.

## How it works

The program uses the popular `github.com/skip2/go-qrcode` library to generate a QR code matrix.  The matrix (`[][]bool`) is then transformed into a string of emojis and printed to stdout.

## Testing

Run the unit tests with:

```bash
go test ./tests/...
```

The test suite checks that the output contains both emoji characters and that the number of lines matches the matrix size.

## License

MIT – see the LICENSE file in the repository root.
