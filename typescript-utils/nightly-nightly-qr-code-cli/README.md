# nightly-qr-code-cli

A tiny TypeScript CLI that turns any input string into a deterministic, whimsical ASCII art representation.

## How it works

1. The input is hashed with SHAâ256.
2. Each hex digit (0âf) is mapped to a pair of Unicode block characters.
3. The resulting patterns are laid out in rows of eight pairs, producing a compact, eyeâcatching block art.

The utility is pure TypeScript, has **no external runtime dependencies** (only Node's builtâin `crypto` module), and can be used as a library or a commandâline tool.

## Installation

```bash
# Clone the repository (or copy this folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-qr-code-cli

# Install dev tools (ts-node & typescript)
npm install
```

## Usage

### As a CLI

```bash
# Run directly with ts-node
npx ts-node src/main.ts "Hello, apocalypse!"
```

### As a library

```ts
import { hashArt } from "./src/main";

const art = hashArt("Hello, apocalypse!");
console.log(art);
```

## Example

```bash
$ npx ts-node src/main.ts "test"
ââââââââââ  ââââ
ââââââââââââââââ
ââââââââââââââ  
ââââââââââ  ââââ
ââââââââââââââââ
ââââ  ââââââââââ
ââââââââââââââââ
ââ  ââ  ââ  ââ
```

## Testing

```bash
npm test
```

The test suite verifies that the deterministic mapping produces the expected art for a known input.

