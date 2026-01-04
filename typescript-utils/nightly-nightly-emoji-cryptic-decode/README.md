# nightly-emoji-cryptic-decoder

Decode a string of emojis into possible textual meanings using a built‑in dictionary.

## Installation

```sh
npm install -g typescript ts-node
```

## Usage

```sh
ts-node src/cli.ts "🐱 🚀 ❤️"
```

Outputs:

```
🐱: cat
🚀: rocket
❤️: love, heart
```

## API

```ts
import { decodeEmojis } from "./decoder";

/**
 * Returns an array of meaning arrays for each emoji token.
 */
const results = decodeEmojis("🐱 🚀 ❤️");
```

## Adding new emojis

Edit `src/decoder.ts` to add entries to the `emojiMap` object.
