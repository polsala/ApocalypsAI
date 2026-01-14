# nightly-clipboard-crypt

**A whimsical yet practical Rust CLI tool** that lets you encrypt or decrypt arbitrary text (think clipboard contents) with a simple passphrase. It uses a reversible XOR cipher combined with Base64 encoding, so the output is safe to paste anywhere.

## Features

- **Encrypt** (`-e`) or **decrypt** (`-d`) data from standard input.
- Passphrase supplied via `-p <pass>` (no storage, just in‑memory).
- Output is plain text (Base64 for encrypted data).
- Zero‑runtime dependencies beyond the standard library and two tiny crates (`clap` for argument parsing, `base64` for encoding).

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
cargo build --release
```

The binary will be located at `target/release/nightly-clipboard-crypt`.

## Usage

```bash
# Encrypt a secret message
echo "my secret" | nightly-clipboard-crypt -e -p "swordfish"
# => bXkgc2VjcmV0IGVuY3J5cHRlZCBzdHJpbmc=

# Decrypt the previous output
echo "bXkgc2VjcmV0IGVuY3J5cHRlZCBzdHJpbmc=" | nightly-clipboard-crypt -d -p "swordfish"
# => my secret
```

You can pipe any text (including clipboard contents via `xclip -o` or `pbpaste`).

## Testing

Run the test suite with:

```bash
cargo test
```

The integration test encrypts a string and then decrypts it, asserting the round‑trip yields the original.

## License

MIT – see LICENSE file.
