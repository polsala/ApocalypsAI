# nightly-emoji-encoder

**Encode** and **decode** arbitrary text to a fun sequence of emojis. Each character is turned into its UTF‑8 byte representation, each byte is expressed as two hexadecimal digits, and each hex digit is mapped to a distinct emoji.

## Install

```bash
# Clone the utility (or let the ApocalypsAI bot add it)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-encoder

# Install dependencies
npm install
```

## Build (optional)

The source is written in TypeScript. You can compile it to JavaScript with:

```bash
npm run build
```

The compiled files will appear in `dist/`. The CLI works directly from the source via `ts-node` as well.

## Usage

```bash
# Encode a string
node ./src/index.ts encode "Hello, world!"

# Decode an emoji string
node ./src/index.ts decode "4️⃣8️⃣6️⃣5️⃣6️⃣c️⃣6️⃣c️⃣..."
```

You can also add the utility to your PATH after building:

```bash
npm link
emoji-encoder encode "Apocalypse"
```

## How it works

| Hex digit | Emoji |
|-----------|-------|
| 0 | 0️⃣ |
| 1 | 1️⃣ |
| 2 | 2️⃣ |
| 3 | 3️⃣ |
| 4 | 4️⃣ |
| 5 | 5️⃣ |
| 6 | 6️⃣ |
| 7 | 7️⃣ |
| 8 | 8️⃣ |
| 9 | 9️⃣ |
| a | 🅰️ |
| b | 🅱️ |
| c | 🆑 |
| d | 🆒 |
| e | 🆓 |
| f | 🆔 |

The mapping is reversible, allowing lossless round‑trips.

## Testing

Run the bundled test suite with:

```bash
npm test
```

All tests should pass, confirming correct encoding/decoding.

