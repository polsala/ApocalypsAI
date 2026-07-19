# nightly-qr-skull-cli

Generate a whimsical ASCII QR‑like code using skull symbols (☠). Useful for embedding a quirky “QR” in terminal logs or chat.

## Install

```sh
npm install -g ts-node typescript
```

## Usage

```sh
npx ts-node src/index.ts "Your message"
```

Outputs a multi‑line skull pattern.

## How it works

Each character of the input is mapped to a 2×2 block:
- Even Unicode code point → skull block (☠)
- Odd code point → empty block (spaces)

Blocks are concatenated horizontally to form the final picture.

## License

MIT
