# nightly-qr-cryptic

A whimsical TypeScript utility that turns any text into an ASCII‑art “QR‑like” code. Not a real QR code, but perfect for post‑apocalyptic notes that need a bit of mystery.

## Installation

```sh
npm install -g nightly-qr-cryptic
```

## Usage

```sh
npx nightly-qr-cryptic "Hello World"
```

Outputs an ASCII block.

## API

```ts
import { generateAsciiQr } from "nightly-qr-cryptic";

const art = generateAsciiQr("Secret");
console.log(art);
```

## How it works

Each character is turned into its 8‑bit binary representation, concatenated, then rendered as a grid of █ (filled) and space (empty) cells, surrounded by a border.
