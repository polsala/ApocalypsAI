Nightly Cryptic Vault

A tiny Rust commandâline tool that lets you encrypt a secret string with a passphrase and store it in a file, then later decrypt it. Useful for quickly stashing notes without leaving them in plain text.

Features
- Simple subcommands: encrypt and decrypt
- Passphraseâderived key using SHAâ256
- AESâ256âGCM encryption with random nonce
- No external services; everything runs locally

Installation
1. Ensure Rust toolchain is installed (rustup).
2. From the utility directory run:
   cargo build --release

Usage
Encrypt a secret (reads from stdin if no --input is given):
   echo "my secret" | cargo run --release -- encrypt --passphrase mypass

Decrypt the previously created vault.bin:
   cargo run --release -- decrypt --passphrase mypass

The encrypted file is named vault.bin by default; you can change it with --output (encrypt) or --input (decrypt).
