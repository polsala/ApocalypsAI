# nightly-void-whisperer-encoder

A TypeScript utility to encode and decode secret messages using the Void-Whisper cipher.

## Usage

```ts
import { encode, decode } from './src/void-whisper-encoder';

const secret = "Apocalypse now!";
const encoded = encode(secret);
console.log(encoded); // Outputs encoded message

const decoded = decode(encoded);
console.log(decoded); // "Apocalypse now!"
```

## CLI

```bash
npx ts-node src/cli.ts encode "Secret message"
npx ts-node src/cli.ts decode "Encoded message"
```
