# nightly-emoji-encoder-cli

A tiny TypeScript CLI that translates plain text into a fun emoji‑based cipher and back again.

## Features

- **Encode** any alphanumeric string (a‑z, 0‑9, space) into a sequence of emojis.
- **Decode** the emoji sequence back to the original text.
- Zero runtime dependencies – just Node.js (v14+).

## Installation

```bash
npm install -g nightly-emoji-encoder-cli
```

## Usage

```bash
# Encode a phrase
nemoji encode "hello world"
# ➜ 🏐📧♓📧   🔱⚱️⚱️📧

# Decode the emoji string
nemoji decode "🏐📧♓📧   🔱⚱️⚱️📧"
# ➜ hello world
```

> **Note**: Characters without a defined mapping are left unchanged.

## Development

```bash
# Install dependencies (only TypeScript for building)
npm install
# Build
npm run build
# Run tests
npm test
```

## License

MIT © ApocalypsAI Community
