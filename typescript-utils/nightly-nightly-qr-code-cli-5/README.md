# nightly-qr-code-cli

Generate an ASCII QR code from any input string.

## Installation

```sh
npm install -g .
```

## Usage

```sh
npx nightly-qr-code-cli "Hello, apocalypse!"
```

Outputs an ASCII QR code that can be scanned from the terminal.

## How it works

Uses the `qrcode-terminal` library to render QR codes as text.
