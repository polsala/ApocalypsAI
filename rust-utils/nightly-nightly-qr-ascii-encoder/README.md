# nightly-qr-ascii-encoder

Generates QR codes as ASCII art for easy sharing in terminal.

## Usage

```sh
cargo run --quiet -- "Hello, world!"
```

The program prints a QR code using `██` for dark modules and two spaces for light modules.

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
