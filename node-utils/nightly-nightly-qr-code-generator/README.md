# nightly-qr-code-generator

A tiny Node.js utility that turns any text into a deterministic ASCII‑art "QR" code.  It is **whimsical** (the pattern is not a real QR code) but **useful** for quickly visualising data in a terminal or embedding it in plain‑text messages.

## Installation

```bash
# Clone the repository (or copy the generated folder) and install dependencies
npm install
```

> No external QR libraries are used – the implementation is pure JavaScript and works offline.

## Usage

```bash
node src/index.js "Hello, world!"
```

The command prints an ASCII block representation where each character is rendered as an 8‑pixel row of `█` (on) and space (off) based on its binary code.

### Example output

```text
 █    █
█ █   █
█ █   █
█ █   █
█ █   █
█ █   █
█ █   █
█ █   █
```

*(The above corresponds to the string `A`.)*

## API

The module exports a single function:

```js
generateQR(text: string): string
```

It returns the multi‑line ASCII representation.

## Testing

```bash
npm test
```

The test suite checks that the generated pattern matches the expected output for known inputs.
