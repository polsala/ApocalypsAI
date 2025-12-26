# nightly-emoji-crypt-decoder

A whimsical utility that encodes and decodes messages using a fixed emoji substitution cipher. Perfect for secret notes in post‑apocalyptic chatrooms.

## Install

```sh
npm install -g nightly-emoji-crypt-decoder
```

## Usage

```sh
# Encode a message
npx nightly-emoji-crypt-decoder encode "HELLO WORLD"
# => 🏱🦁📧🦁🦁/⚽🦁🌛🦁📧

# Decode a message
npx nightly-emoji-crypt-decoder decode "🅰️🅱️🌜"
# => ABC
```

## API

```ts
export function encode(text: string): string;
export function decode(emojis: string): string;
```

* `encode` converts plain‑text (A‑Z, spaces) into a string of emojis. Spaces become `/` to preserve word boundaries.
* `decode` reverses the process, turning `/` back into spaces.

## Development

```sh
# Install dependencies
npm install

# Run tests
npm test
```

## License

MIT
