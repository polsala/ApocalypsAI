# Cryptic Chronicle

A whimsical CLI tool for the post‑apocalyptic archivist. It encrypts a short message with a secret key, stamps it with the current Unix timestamp, and outputs a base64 string. Later you can decrypt it to retrieve the original message and see when it was sealed.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Encrypt
cryptic-chronicle encrypt --key mysecret "Remember the sunrise"

# Decrypt
cryptic-chronicle decrypt --key mysecret <base64-string>
```

## How it works

- The message is XOR‑ed with the provided key (repeating as needed).
- The current Unix timestamp (seconds) is prepended (big‑endian).
- The resulting bytes are base64‑encoded.

## License

MIT
