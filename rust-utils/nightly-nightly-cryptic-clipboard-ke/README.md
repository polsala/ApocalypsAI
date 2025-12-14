# Nightly Cryptic Clipboard Keeper

A whimsical CLI tool that encrypts or decrypts text (e.g., clipboard contents) using a simple XOR‑based cipher and Base64 encoding. Perfect for quick secret sharing without leaving traces.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Encrypt
echo "my secret" | nightly-cryptic-clipboard-keeper encrypt "myPass"

# Decrypt
echo "c2VjcmV0..." | nightly-cryptic-clipboard-keeper decrypt "myPass"
```

## How it works

- XOR each byte with a repeating key derived from the passphrase.
- Encode the result with Base64 for safe transport.
- Decryption reverses the process.

## License

MIT
