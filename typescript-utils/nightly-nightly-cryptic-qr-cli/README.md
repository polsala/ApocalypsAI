# nightly-cryptic-qr-cli

A whimsical CLI utility that generates a simple ASCII‑art “QR‑like” code from any input string. The pattern is deterministic and uses only `#` or `@` characters, making it safe for terminal display without external dependencies.

## Installation

```sh
npm install -g ts-node typescript
```

## Usage

```sh
npx ts-node src/index.ts "your secret message"
```

The tool prints an ASCII box whose interior is filled with `#` (for even‑hash inputs) or `@` (for odd‑hash inputs).

## Example

```sh
$ npx ts-node src/index.ts test
+------+
|######|
|######|
|######|
+------+
```

## API

```ts
import { generateQrAscii } from "./qr";

/**
 * Returns an ASCII‑art representation of a pseudo‑QR code for the given text.
 */
const art = generateQrAscii("hello");
```
