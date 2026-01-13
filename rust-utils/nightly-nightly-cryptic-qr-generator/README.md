# Nightly Cryptic QR Generator

**Generate QR codes as ASCII art from any input string.**

## Overview

This tiny Rust CLI takes a piece of text and prints a QR code made of Unicode fullâblock characters (â) and spaces. It works entirely in the terminal â no image files required.

## Installation

You need a Rust toolchain (rustc and cargo). Then clone the repository and build the binary:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-cryptic-qr-generator
cargo build --release
```

The compiled binary will be at `target/release/cryptic_qr_generator`.

## Usage

```bash
# Print QR for a short message
cargo run -- "Hello, apocalypse!"

# Or use the built binary directly
./target/release/cryptic_qr_generator "https://example.com"
```

The program prints an ASCII QR code to stdout.

## Example

```text
ââââââââââââââââââââ
â â  â â â  â â â â
â â â â â â â â â â
â   â   â   â   â â
ââââââââââââââââââââ
```

## License

MIT License â see LICENSE file in the repository.

