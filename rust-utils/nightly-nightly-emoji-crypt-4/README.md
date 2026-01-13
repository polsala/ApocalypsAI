# nightly-emoji-crypt

A whimsical CLI tool that encodes and decodes arbitrary text to a sequence of emojis, using a custom 64‑character emoji alphabet. Useful for secret messages, fun chats, or hiding passwords in plain sight.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Encode a string
emoji-crypt encode "Hello, world!"

# Decode back
emoji-crypt decode "😀😃😄..."
```

## How it works

The tool maps each 6‑bit chunk of the input (like Base64) to an emoji from a fixed alphabet of 64 emojis. Decoding reverses the process.

## License

MIT
