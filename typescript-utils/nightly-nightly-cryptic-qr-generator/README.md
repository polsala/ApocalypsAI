# Nightly Cryptic QR Generator

A whimsical command‑line utility that converts a short piece of text into an ASCII‑style QR‑like code using custom symbols. Great for sharing secret messages in terminal chats.

## Installation

```bash
npm install -g ts-node typescript
```

*(The utility has no external runtime dependencies.)*

## Usage

```bash
npx ts-node src/main.ts "Your message"
```

The tool will print an ASCII art block representing the input.

## Example

```bash
npx ts-node src/main.ts "AB"
```

Output:

```
@@..
..**
```

## How it works

Each character is mapped to a 2×2 pattern of symbols chosen from a small set. The patterns are concatenated horizontally to form a two‑row “QR” code.
