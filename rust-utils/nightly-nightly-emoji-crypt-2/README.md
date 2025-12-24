# nightly-emoji-crypt

A whimsical Rust CLI that translates plain text into a sequence of emojis and back again. Great for secret notes, fun chats, or adding a splash of personality to logs.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Encode a message
nightly-emoji-crypt encode "hello world"

# Decode a message
nightly-emoji-crypt decode "😀😆😃😃😗⬜😐😗😃😑"
```

## How it works

Each alphabetic character (a‑z) and space is mapped to a unique emoji. Characters outside the supported set are replaced with the “❓” placeholder during encoding and become “?” after decoding.
