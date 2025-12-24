# nightly-clipboard-crypt

A whimsical CLI tool that encrypts or decrypts the text currently in your system clipboard using a simple XOR‑based cipher and Base64 encoding. Perfect for quickly sharing secrets in a post‑apocalyptic chat.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Encrypt clipboard contents with passphrase "s3cr3t"
nightly-clipboard-crypt encrypt s3cr3t

# Decrypt clipboard contents with the same passphrase
nightly-clipboard-crypt decrypt s3cr3t
```

The tool reads the clipboard, transforms the text, writes the result back to the clipboard, and also prints it to stdout.

## How it works

- Derives a repeating key from the UTF‑8 bytes of the passphrase.
- XORs each byte of the input with the key byte.
- Encodes the result with Base64 for the encrypted form.
- Decryption reverses the process.

## License

MIT
