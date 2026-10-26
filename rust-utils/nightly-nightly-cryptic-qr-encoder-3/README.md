# nightly-cryptic-qr-encoder

A whimsical CLI tool that converts a given string into an ASCII (Unicode block) QR code, printable in any terminal.

## Usage

```sh
cargo run -- <text>
```

Example:

```sh
cargo run -- "Hello, world!"
```

Outputs a QR code made of █ and space characters.

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
