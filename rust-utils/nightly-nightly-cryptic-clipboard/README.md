Nightly Cryptic Clipboard

A whimsical Rust CLI tool that encrypts or decrypts arbitrary text using a simple XOR cipher with a passphrase, encoding the result in Base64. Perfect for quick secret notes in a postâapocalyptic chat.

Installation:
- Ensure Rust toolchain is installed.
- Run `cargo install --path .` inside the utility directory.

Usage:
  nightly-cryptic-clipboard encrypt <passphrase> <plain-text>
  nightly-cryptic-clipboard decrypt <passphrase> <base64-cipher>

Example:
  $ nightly-cryptic-clipboard encrypt secret "Meet at dusk"
  bXl... (Base64 output)
  $ nightly-cryptic-clipboard decrypt secret bXl...
  Meet at dusk

Note: This is NOT cryptographically secure; it's for fun.
