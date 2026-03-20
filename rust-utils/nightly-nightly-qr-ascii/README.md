# nightly-qr-ascii

Generate a QR code from any text and display it as ASCII art directly in your terminal.

## Installation

```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-qr-ascii

# Build the binary using Cargo
cargo build --release
```

The compiled binary will be located at `target/release/nightly-qr-ascii`.

## Usage

```bash
# Basic usage – provide the text you want to encode as the sole argument
./target/release/nightly-qr-ascii "Hello, world!"
```

The program prints an ASCII representation of the QR code to stdout. If you omit the argument, it prints a short usage message.

## How it works

The tool uses the pure‑Rust `qrcode` crate to generate a QR matrix and then renders it with the `unicode::Dense1x2` renderer, mapping dark modules to the block character `█` and light modules to a space.

## Testing

Run the test suite with:

```bash
cargo test
```

The tests verify that the generator produces non‑empty output containing block characters for a sample input.

## License

MIT © ApocalypsAI community
