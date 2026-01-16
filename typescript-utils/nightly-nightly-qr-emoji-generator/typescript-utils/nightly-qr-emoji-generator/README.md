# nightly-qr-emoji-generator

A whimsical TypeScript CLI that turns any text into a pseudo‑QR code made of ASCII characters. Perfect for sharing secret messages in the apocalypse‑proof terminal.

## Install

```sh
npm install -g nightly-qr-emoji-generator
```

## Usage

```sh
npx nightly-qr-emoji-generator "Hello World"
```

The command prints an ASCII art block representing the input text.

## How it works

The tool converts each character to its UTF‑16 code point, then maps each bit to a 2×2 block:
- `0` → space
- `1` → `█`

Blocks are arranged row‑major to form a square grid, yielding a deterministic, deterministic‑looking QR‑like pattern.

## License

MIT
