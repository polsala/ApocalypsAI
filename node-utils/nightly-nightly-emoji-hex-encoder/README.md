# nightly-emoji-hex-encoder

Encode and decode strings to a whimsical emoji representation of hexadecimal data.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js encode "Hello World"
# => 😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰🤩 (example output)

node src/index.js decode "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰🤩"
# => Hello World
```

## How it works

Each hexadecimal digit (0‑f) is mapped to a unique emoji. The utility converts the input string to UTF‑8 bytes, then to hex, then to emojis. Decoding reverses the process.

## License

MIT
