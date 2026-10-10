# nightly-cryptic-qr-encoder

A tiny Rust CLI that turns any text into an ASCII QR code printed to the terminal.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
nightly-cryptic-qr-encoder "Hello, world!"
```

Outputs a QR code made of █ and space characters.

## How it works

Uses the `qrcode` crate to generate a QR code and renders it as Unicode block characters.

## Testing

Run `cargo test`.
