# Wasteland QR

A tiny Rust CLI that turns any text into an ASCII QR code, perfect for passing secret messages in the post‑apocalypse.

## Usage

```sh
# Build the binary
cargo build --release

# Generate a QR code for a string
./target/release/wasteland-qr "HELLO WORLD"

# Or pipe input from stdin
echo "HELLO" | ./target/release/wasteland-qr
```

The tool prints the QR code using Unicode block characters, making it easy to copy‑paste into terminal chats or printed notes.

## Testing

```sh
cargo test
```

## Implementation Details

The utility relies on the `qrcode` crate to generate a QR code matrix and renders it with the `Dense1x2` Unicode renderer, which uses the characters `█` and space to represent dark and light modules.
