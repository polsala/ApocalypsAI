# nightly-rot13-emoji-encoder

A tiny TypeScript CLI utility that:

1. Applies the classic ROT13 cipher to the input text.
2. Replaces each alphabetic character with a corresponding emoji (a‑z → 26 unique emojis).
3. Leaves non‑alphabetic characters untouched.

The result is a whimsical, emoji‑filled string that can be decoded back to the original text by running the tool again (ROT13 is its own inverse).

## Installation

```bash
# Clone the repository (or copy the generated folder) and install dependencies
npm install -g ts-node typescript
```

> **Note**: The utility has no external runtime dependencies beyond the TypeScript compiler and `ts-node` for execution.

## Usage

```bash
# Encode a string passed as an argument
npx ts-node src/main.ts "Hello, World!"
```

Output (example):

```
⛎🌈🪁🪁🅱️🕹️🅱️📧🪁🍳, 🪁⚽🛴🛴🅱️!
```

If no argument is supplied, the tool reads from STDIN:

```bash
echo "Secret Message" | npx ts-node src/main.ts
```

## API

The module exports two pure functions that can be imported in other TypeScript/JavaScript projects:

```ts
export function rot13(input: string): string;
export function encodeToEmoji(input: string): string;
```

- `rot13` – classic ROT13 transformation.
- `encodeToEmoji` – performs ROT13 then maps letters to emojis.

## Testing

Run the bundled tests with:

```bash
npx ts-node tests/test_main.ts
```

All tests should pass without network access.
