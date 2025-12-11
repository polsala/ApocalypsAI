# nightly-qr-code-cli

Generate QR codes directly in your terminal.

## Overview

`nightly-qr-code-cli` is a tiny TypeScript command‑line tool that takes a string and prints a QR code using Unicode block characters. It supports a `--small` flag for a more compact representation.

## Installation

```sh
npm install -g ts-node qrcode-terminal
```

Or run without installing globally:

```sh
npx ts-node src/main.ts "Hello world"
```

## Usage

```sh
npx ts-node src/main.ts "<text>" [--small]
```

* `<text>` – The text to encode.
* `--small` – (optional) Produce a smaller QR code.

## Example

```sh
npx ts-node src/main.ts "Apocalypse"
```

Outputs a QR code that can be scanned from the terminal.

## Testing

Run the tests with:

```sh
npx ts-node tests/test_main.ts
```

The test suite mocks the QR generation to ensure deterministic results.
