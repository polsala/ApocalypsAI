# nightly-qr-ascii-art

Generate QR codes as ASCII art directly from the command line.

## Build

```sh
cargo build --release
```

## Usage

```sh
# Pipe input
echo "Hello, world!" | nightly-qr-ascii-art
```

or

```sh
nightly-qr-ascii-art "Hello, world!"
```

The program prints the QR code using `██` for black modules and two spaces for white modules.

## Test

```sh
cargo test
```
