# Nightly Crypto Cipher Box

A whimsical CLI tool for encrypting and decrypting messages using a custom substitution cipher with a configurable alphabet and key.

## Features

- Encrypt and decrypt messages using a custom substitution cipher
- Configurable alphabet and key
- Whimsical and fun output

## Installation

1. Clone this repository
2. Navigate to the `nightly-crypto-cipher-box` directory
3. Run `cargo build --release`
4. The binary will be located at `target/release/nightly-crypto-cipher-box`

## Usage

### Encrypt a message

```bash
nightly-crypto-cipher-box encrypt "Hello, World!"
```

### Decrypt a message

```bash
nightly-crypto-cipher-box decrypt "Khoor, Zruog!"
```

### Custom alphabet and key

```bash
nightly-crypto-cipher-box encrypt "Hello, World!" --alphabet "abcdefghijklmnopqrstuvwxyz" --key 3
```

## License

MIT License
