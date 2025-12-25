# nightly-cryptic-qr-encoder

A tiny Rust CLI that converts a given string into an ASCII QR code. Useful for embedding short messages in terminal‑friendly format without external image viewers.

## Usage

```sh
cargo run --quiet -- <text>
```

Example:

```sh
cargo run -- "HELLO"
```

Outputs an ASCII QR code.

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
