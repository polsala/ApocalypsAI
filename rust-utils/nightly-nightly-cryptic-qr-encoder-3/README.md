# nightly-cryptic-qr-encoder

A tiny Rust CLI that converts a given text into an ASCII QR code, perfect for sharing secrets over a terminal.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
nightly-cryptic-qr-encoder "Hello, world!"
```

The program will print an ASCII representation of the QR code to stdout.

## Example

```sh
$ nightly-cryptic-qr-encoder "HELLO"
█████████████████████████
██ ▄▄▄▄▄ █ ▄ █ ▄▄▄▄▄ ██
██ █   █ █ █ █ █   █ ██
██ █▄▄▄█ █ █ █ █▄▄▄█ ██
██▄▄▄▄▄▄▄█ █ █▄▄▄▄▄▄▄██
██ ▄ █ ▄ █ █ █ ▄ █ ▄ ██
██ █ █ █ █ █ █ █ █ █ ██
██ ▀ █ ▀ █ █ █ ▀ █ ▀ ██
██▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██
█████████████████████████
```

*(The exact pattern may vary depending on the QR version used.)*

## License

MIT
