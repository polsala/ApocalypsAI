# nightly-qr-ansi-art

Generate a whimsical QR‑like ASCII art from any text. The tool converts each character to an 8‑bit binary row, displaying `█` for 1 and a space for 0. Perfect for adding a retro‑tech flair to logs, commit messages, or terminal greetings.

## Installation

```sh
npm install -g nightly-qr-ansi-art
```

## Usage

```sh
npx nightly-qr-ansi-art "Hello"
```

Outputs something like:

```
 █   █ █
█ █ █  █
...
```

## API

```ts
import { generate } from "nightly-qr-ansi-art";

const art = generate("Secret");
console.log(art);
```

## License

MIT
