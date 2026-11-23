# nightly-emoji-decoder

A tiny Rust CLI that translates emojis into short textual descriptions.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
emoji-decoder "🚀🌕"
```

Outputs:

```
🚀 -> rocket
🌕 -> full moon
```

If no argument is supplied, the tool reads from **STDIN**.

## Supported emojis

| Emoji | Description |
|-------|-------------|
| 🚀 | rocket |
| 🌕 | full moon |
| 🔥 | fire |
| 💧 | droplet |
| ⚡ | high voltage |
| ❤️ | heart |
| 😂 | joy |
| 🤖 | robot |
| 🧩 | puzzle piece |
| 🌟 | star |

## License

MIT © ApocalypsAI
