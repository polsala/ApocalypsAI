# Cryptic Emoji Decoder

A tiny Rust CLI that translates a space‑separated list of emojis into a readable string using a predefined emoji‑to‑letter map. Perfect for playful secret messages in the wasteland.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
cryptic-emoji-decoder 🌞 🌙 🌟
```

Outputs:

```
ABC
```

## Emoji Map

| Emoji | Letter |
|-------|--------|
| 🌞 | A |
| 🌙 | B |
| 🌟 | C |
| 🔥 | D |
| 💧 | E |
| 🌪️ | F |
| 🌈 | G |
| 🍎 | H |
| 🍞 | I |
| 🐍 | J |

Add more as you wish.

## Testing

```sh
cargo test
```
