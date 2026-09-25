# nightly-cryptic-qr-encoder

A tiny Rust CLI that turns any text into an ASCII QR code.

## Build

```sh
cargo build --release
```

## Usage

```sh
./target/release/cryptic-qr-encoder "Hello, world!"
```

The program prints a QR code made of `█` (dark) and spaces (light).

## License

MIT
