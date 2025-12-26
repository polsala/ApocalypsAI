# nightly-emoji-mood-analyzer

A whimsical yet handy command‑line utility that reads a short piece of text and returns an emoji that best matches the overall mood.

## Features

- Zero external dependencies – pure Node.js (v12+).
- Simple sentiment analysis based on curated word lists.
- Works as a one‑liner: `node src/index.js "I love sunny days!"`

## Installation

1. Clone the repository or copy the `src/` folder into your project.
2. Ensure you have Node.js installed (`node -v`).
3. No `npm install` required – the script uses only the built‑in `fs` and `path` modules.

## Usage

```bash
node src/index.js "Your text here"
```

### Examples

```bash
$ node src/index.js "I just got a promotion!"
🎉

$ node src/index.js "I lost my keys again..."
😞

$ node src/index.js "The traffic is terrible today."
😡
```

## How it works

The script tokenises the input, counts occurrences of positive and negative keywords, and decides the dominant sentiment:

- **Positive** → 🎉 (celebration)
- **Negative** → 😞 (sad)
- **Angry**   → 😡 (angry)
- **Neutral/unknown** → 🤔 (thinking)

Feel free to extend the word lists in `src/index.js` to suit your own lexicon.

## Testing

Run the bundled test suite with:

```bash
node tests/test.js
```

All tests should pass, confirming correct emoji selection for a variety of inputs.
