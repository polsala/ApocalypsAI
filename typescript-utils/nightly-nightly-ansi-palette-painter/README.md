# nightly-ansi-palette-painter

A whimsical TypeScript CLI that paints a sample block in the terminal using ANSI escape codes for a given color name or hex value.

## Installation

```sh
npm install -g .
# or run with npx ts-node src/index.ts <color>
```

## Usage

```sh
node dist/index.js red
# or
npx ts-node src/index.ts "#00ff00"
```

Outputs a colored block and the corresponding ANSI code.

## Supported colors

- Basic names: black, red, green, yellow, blue, magenta, cyan, white
- Hex strings like "#ff00ff"

## Development

Run tests:

```sh
npm test
```
