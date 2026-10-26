# nightly-qr-code-artist

A tiny Rust CLI that converts any input text into an ASCII‑style QR code using block characters. Great for sharing short strings in terminals, chat, or printed notes.

## Build

```sh
cargo build --release
```

## Usage

```sh
cargo run -- "Hello, world!"
```

or after building:

```sh
./target/release/qr-code-artist "Hello, world!"
```

The program prints the QR code made of `██` for dark modules and two spaces for light modules.

## Testing

```sh
cargo test
```
