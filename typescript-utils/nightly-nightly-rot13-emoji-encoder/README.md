# Nightly ROT13 Emoji Encoder

## Overview

`nightly-rot13-emoji-encoder` is a tiny, whimsical commandâline utility written in TypeScript. It takes an input string, applies the classic ROT13 cipher, and then prefixes each resulting character with an emoji chosen deterministically from a small palette. The result is a fun, readable âemojiâcipherâ that can be shared in chat, logs, or anywhere you need a lightâhearted obfuscation.

## Features

- Pure TypeScript implementation â no native dependencies.
- Deterministic emoji selection (same input always yields the same output).
- Works as a library (`encodeWithEmoji`) or as a CLI tool.

## Installation

You can run the utility directly with `ts-node` (recommended for quick use) or compile it to JavaScript.

```bash
# Using ts-node (you need it installed globally or in your project)
npm install -g ts-node typescript

# Clone the repository and run
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-rot13-emoji-encoder
ts-node src/main.ts "Hello, World!"
```

If you prefer a compiled version:

```bash
# Compile to JavaScript
npm install -g typescript
tsc src/main.ts --outDir dist
node dist/main.js "Hello, World!"
```

## Usage

### CLI

```bash
# Encode a string passed as an argument
ts-node src/main.ts "Your message here"
```

If no argument is supplied, the tool reads from STDIN:

```bash
echo "Secret" | ts-node src/main.ts
```

### Library

You can import the core function in other TypeScript/JavaScript projects:

```ts
import { encodeWithEmoji } from "./src/main";

const encoded = encodeWithEmoji("Hello");
console.log(encoded); // ð§Uð¥rðyðyâ¡b
```

## Example

```bash
$ ts-node src/main.ts "Hello"
ð§Uð¥rðyðyâ¡b
```

## Testing

The utility ships with a small Jest test suite. Run the tests with:

```bash
npm install
npm test
```

## License

MIT â see the LICENSE file in the repository root.

