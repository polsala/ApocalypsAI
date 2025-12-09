# nightly-emoji-qr

**nightly-emoji-qr** is a tiny, whimsical utility that turns any string into an emoji‑filled square that looks a bit like a QR code.  It’s purely for fun – you can copy‑paste the output into chat, forums, or a terminal and watch the emojis dance.

## Install

The utility is written in TypeScript but ships a pre‑compiled JavaScript file, so you can run it with plain Node.js (>=14).

```bash
# Clone the repository (or copy the utility folder) and install dependencies if you want to rebuild the TypeScript source
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/typescript-utils/nightly-emoji-qr
# No runtime dependencies required
```

## Usage

```bash
# Run the compiled JavaScript directly
node src/index.js "Your message here"
```

If you omit the argument, the utility will read from **STDIN**:

```bash
echo "Hello" | node src/index.js
```

### Example

```bash
node src/index.js "AB"
```

Output:

```
😃😄
😀😀
```

## How it works

1. The input string is split into characters.
2. Each character’s Unicode code point is mapped to one of eight emojis.
3. The characters are placed into a square grid (size = ceil(sqrt(length))) and padded with spaces if necessary.
4. The grid is printed line‑by‑line.

Feel free to tweak the emoji palette in `src/index.ts`!

## Testing

Run the bundled test script:

```bash
bash tests/test_main.sh
```

The test checks that a known input produces the expected emoji grid.
