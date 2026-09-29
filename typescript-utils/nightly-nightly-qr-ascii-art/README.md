# nightly-qr-ascii-art

Generate a simple ASCII art representation of a QR‑like code from any text.

## Usage

```sh
npx nightly-qr-ascii-art "Hello"
```

## API

```ts
import { generateAsciiQr } from 'nightly-qr-ascii-art';

const art = generateAsciiQr('Hello');
console.log(art);
```

The function converts each character to its 8‑bit binary representation and maps `1` to a solid block (`█`) and `0` to a space.
