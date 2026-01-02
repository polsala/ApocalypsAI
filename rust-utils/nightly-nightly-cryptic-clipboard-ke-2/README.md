# nightly-cryptic-clipboard-keeper

A whimsical Rust CLI that encrypts or decrypts text (e.g., your clipboard) using a simple XOR cipher with a passphrase. Perfect for secret notes that vanish into the void.

## Installation

```sh
cargo install --path .
```

## Usage

Encrypt from stdin:

```sh
echo "Secret message" | nightly-cryptic-clipboard-keeper encrypt mypass > encrypted.txt
```

Decrypt:

```sh
cat encrypted.txt | nightly-cryptic-clipboard-keeper decrypt mypass
```

## How it works

The tool reads all input, XOR‑s each byte with the repeating bytes of the passphrase, and outputs the result. The same operation is used for encryption and decryption.

## Safety note

This is **not** cryptographically secure; it is just for fun.
