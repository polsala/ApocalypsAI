# Nightly Cryptic QR Generator

A whimsical TypeScript CLI that turns any text into an ASCII QR code.
Optionally wraps the QR in a post‑apocalypse styled border.

## Install

```sh
npm install -g nightly-cryptic-qr
```

## Usage

```sh
nightly-cryptic-qr "Hello world"
nightly-cryptic-qr "Secret" --border
```

## API

```ts
import { generateAsciiQR } from 'nightly-cryptic-qr';

const qr = generateAsciiQR('Message', { border: true });
```

## How it works

Uses the `qrcode-terminal` package to generate QR codes in the terminal.
When `border` is true, the output is surrounded by a decorative border
made of the `⛧` rune and horizontal lines.

## Tests

Run `npm test` to execute the Jest test suite.
