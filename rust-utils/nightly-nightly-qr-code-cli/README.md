# nightly-qr-code-cli

Generate QR codes as ASCII art from the command line.

## Installation

```sh
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-qr-code-cli

# Build the binary
cargo build --release
```

The compiled binary will be located at `target/release/qr-code-cli`.

## Usage

```sh
qr-code-cli "Hello, world!"
```

The program prints an ASCII representation of the QR code to stdout.

## Testing

```sh
cargo test
```

## License

MIT © ApocalypsAI community
