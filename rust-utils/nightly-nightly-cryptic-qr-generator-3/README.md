# nightly-cryptic-qr-generator

A tiny Rust CLI that generates QR codes as ASCII art. It can optionally reverse the input text to hide the message.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
cryptic-qr "Hello World"
cryptic-qr -r "Secret"
```

### Options

- `-r, --reverse` : reverse the input before encoding.

## Example

```sh
cryptic-qr "Apocalypse"
```

The command prints an ASCII QR code to the terminal.
