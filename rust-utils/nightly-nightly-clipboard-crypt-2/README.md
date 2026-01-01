# nightly-clipboard-crypt

A whimsical Rust CLI tool that encrypts text (e.g., clipboard contents) with a simple XOR cipher and saves it to a file, and can later decrypt it. Useful for quick, reversible obfuscation without external dependencies.

## Usage

```sh
# Encrypt text from stdin and write to encrypted.bin
echo "Secret message" | nightly-clipboard-crypt encrypt mykey encrypted.bin

# Decrypt and output to stdout
nightly-clipboard-crypt decrypt mykey encrypted.bin
```

## How it works

The tool XOR‑s each byte of the input with the repeating key bytes, then writes the raw bytes to the output file. Decryption performs the same operation.

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
