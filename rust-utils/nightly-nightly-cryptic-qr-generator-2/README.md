# nightly-cryptic-qr-generator

A tiny Rust CLI that converts a short text into an ASCII QR code. Useful for embedding links in terminal chats, README files, or just for fun.

## Usage

```sh
cargo run --quiet -- "Hello, world!"
```

The program prints an ASCII QR code to stdout.

## Build

```sh
cargo build --release
```

## License

MIT
