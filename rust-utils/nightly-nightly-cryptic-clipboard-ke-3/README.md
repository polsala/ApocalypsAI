# Cryptic Clipboard Keeper

A tiny Rust CLI tool that encrypts or decrypts data from stdin using a passphrase. Perfect for quickly securing clipboard contents before sharing.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Encrypt
echo "secret message" | cryptic-clipboard -e mypass > encrypted.bin

# Decrypt
cat encrypted.bin | cryptic-clipboard -d mypass
```

## How it works

Uses a simple XOR cipher with the passphrase repeated to match the data length. Not suitable for high‑security needs, but fun for casual obfuscation.

## License

MIT
