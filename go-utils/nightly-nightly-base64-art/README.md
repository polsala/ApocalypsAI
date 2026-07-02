# nightly-base64-art

A whimsical command‑line utility that takes a string, encodes it in Base64 and displays each character as a colored block in the terminal. Useful for quick visual checks or adding a splash of color to logs.

## Installation

```sh
go build -o nightly-base64-art ./src
```

## Usage

```sh
echo "Hello, world!" | nightly-base64-art
# or
nightly-base64-art "some text"
```

## How it works

Each Base64 character is mapped to one of 64 ANSI colors. The program prints a full‑block character (`█`) with the corresponding foreground color.

## License

MIT
