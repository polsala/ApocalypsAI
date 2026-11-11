# nightly-emoji-decoder

A whimsical Node.js CLI that translates a string of emojis into letters using a secret mapping. Unknown emojis become "?".

## Installation

```sh
npm install -g .
```

## Usage

```sh
emoji-decoder 😀😁😂
# => ABC
```

You can also pipe input:

```sh
echo "😀😁😂" | emoji-decoder
```

## How it works

Each supported emoji maps to a letter (A‑J). The mapping is defined in `src/decoder.js`. The tool iterates over the input characters and builds the decoded string.

## Testing

```sh
node tests/test_decoder.js
```

## License

MIT
