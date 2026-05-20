# Nightly QR ASCII Art

Convert a short string into a tiny QR‑like ASCII art block.

## Install

```sh
npm install -g nightly-qr-ascii-art
```

## Usage

```sh
nqr "Hello"
```

Outputs a 2‑row ASCII representation.

## How it works

Each character is turned into a 2×2 block based on the lowest four bits of its UTF‑16 code unit. The blocks are concatenated horizontally.
