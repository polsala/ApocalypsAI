# nightly-qr-reverse-decoder

A tiny Rust command‑line tool that decodes a playful QR representation.

## What is a "QR" here?
For the sake of fun, the QR format is **just** a string that:
1. Starts with the literal prefix `QR:`
2. Is followed by the original message written **backwards**.

Example encoded string:
```
QR:!dlroW ,olleH
```
Decodes to:
```
Hello, World!
```

## Build
```bash
# From the utility root directory
cargo build --release
```
The binary will be placed at `target/release/qr-reverse-decoder`.

## Usage
```bash
# Encode your message in the whimsical QR format and write it to a file
echo "QR:!dlroW ,olleH" > example.qr

# Run the decoder
./target/release/qr-reverse-decoder example.qr
# => Hello, World!
```

## Testing
```bash
cargo test
```
All tests are deterministic and run offline.
