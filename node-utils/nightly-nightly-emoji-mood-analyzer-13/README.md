# nightly-emoji-mood-analyzer

A tiny, whimsical utility that scans a piece of text and returns an emoji that reflects the overall mood.

## Features

- Simple sentiment analysis based on a handcrafted word list.
- Works as a command‑line tool or as a library function.
- Zero external dependencies – just Node.js built‑ins.

## Installation

```bash
# Clone the repository (or copy the utility into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-analyzer
npm install   # installs dev dependencies for testing only
```

## Usage

### CLI

```bash
node src/index.js <path-to-text-file>
```

If no file is provided, the utility reads from **STDIN**.

### Library

```javascript
const { analyzeMood } = require('./src/index');
const mood = analyzeMood('I love sunny days but hate rain.');
console.log(mood); // 😐
```

## How It Works

The analyzer tokenises the input text, counts occurrences of a small set of positive and negative words, and decides the mood:

- More positive words → 😊
- More negative words → 😢
- Tie or none → 😐

## Testing

Run the test suite with:

```bash
npm test
```

The tests are deterministic and do not require any network access.

## License

MIT © ApocalypsAI
