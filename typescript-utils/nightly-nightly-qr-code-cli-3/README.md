# nightly-qr-code-cli

Generate a QRâcodeâlike visual in your terminal from any text.

## Install

```sh
npm install -g nightly-qr-code-cli
```

## Usage

```sh
npx nightly-qr-code-cli "Hello, world!"
```

Outputs a blockâcharacter representation of a QR code (placeholder implementation).

## API

```ts
import { generateQr } from "nightly-qr-code-cli";

const art = generateQr("Hello");
console.log(art);
```

## How it works

The library encodes the input string into a deterministic pattern of Unicode block
characters. It is **not** a real QR code; it is a whimsical visual for fun
and debugging.

## Testing

```sh
npm test
```
