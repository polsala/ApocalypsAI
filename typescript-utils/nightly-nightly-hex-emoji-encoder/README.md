# nightly-hex-emoji-encoder

A tiny TypeScript CLI that converts any UTF‑8 string into a sequence of emojis representing its hexadecimal bytes, and back again. Perfect for sharing secret messages in a post‑apocalyptic chat where only emojis survive.

## Install

```bash
npm install -g typescript ts-node
npm install -g nightly-hex-emoji-encoder
```

> The utility is a single TypeScript file; you can also run it directly with `ts-node` if you prefer not to install globally.

## Usage

```bash
# Encode a string
hex-emoji-encoder "Hello World"
# => 48️⃣65️⃣6c️⃣6c️⃣6f️⃣20️⃣57️⃣6f️⃣72️⃣6c️⃣64️⃣

# Decode an emoji string
hex-emoji-encoder --decode "48️⃣65️⃣6c️⃣6c️⃣6f️⃣20️⃣57️⃣6f️⃣72️⃣6c️⃣64️⃣"
# => Hello World
```

The tool reads the first argument as the text to encode, or, when `--decode` is supplied, reads the second argument as the emoji‑encoded string.

## API

You can also import the functions in your own TypeScript project:

```ts
import { encodeToEmoji, decodeFromEmoji } from 'nightly-hex-emoji-encoder';

const secret = encodeToEmoji('Secret');
const original = decodeFromEmoji(secret);
```

## Testing

Run the bundled tests with:

```bash
npm test
```

The tests verify the mapping table and a full round‑trip conversion.
