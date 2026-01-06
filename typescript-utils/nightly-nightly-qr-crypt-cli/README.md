# nightly‑qr‑crypt‑cli

A whimsical yet handy command‑line utility written in TypeScript that:

1. **Applies a Caesar‑cipher shift** to a supplied string (default shift = 1).
2. **Generates a QR‑code‑style representation** of the shifted text and prints it to the terminal.

The QR output is a simple placeholder (`QR:<shifted‑text>`) so the tool works without external native dependencies, making it perfect for quick, offline demos or scripting.

---

## Installation

```bash
# Clone the repository (or copy the generated folder) and install dependencies
npm install
```

> The utility has **no runtime dependencies** beyond the Node standard library, so `npm install` merely creates a `node_modules` folder for the dev‑dependency `typescript` used during compilation.

## Build

```bash
npx tsc
```

This compiles the TypeScript source in `src/` to JavaScript in `dist/`.

## Usage

```bash
node dist/index.js "Hello, world!" -s 3
```

* `"Hello, world!"` – the text to encode.
* `-s 3` – optional shift amount (defaults to 1).

**Example output**

```
QR:Khoor, zruog!
```

---

## Testing

```bash
npm test
```

The test suite lives in `tests/` and validates the Caesar shift and QR placeholder logic.
