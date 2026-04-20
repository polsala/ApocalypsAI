# nightly-qr-ascii-generator

A tiny, whimsical utility written in TypeScript that converts an input string into a QR‑like ASCII art representation.  It’s **not** a real QR code generator – it simply creates a deterministic pattern based on the character codes, making it perfect for quick, fun terminal sharing.

## Features

- Zero‑dependency TypeScript implementation.
- Works as a CLI (`node src/index.js "your text"`).
- Exposes a `generateAsciiArt(text: string): string` function for programmatic use.
- Fully typed and includes a deterministic test suite.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install TypeScript globally if you don’t have it
npm install -g typescript ts-node
```

## Usage

```bash
# Run the CLI directly with ts-node (no compilation needed)
ts-node src/index.ts "Hello World"
```

The above command will output something like:

```
██  ██  ██  ██  ██  ██
██  ██  ██  ██  ██  ██
```

## API

```ts
import { generateAsciiArt } from "./src/index";

const art = generateAsciiArt("Apocalypse");
console.log(art);
```

## Testing

```bash
# Run the test with ts-node (no test runner required)
ts-node tests/test_index.ts
```

The test will exit silently on success or throw an error if the output differs.
