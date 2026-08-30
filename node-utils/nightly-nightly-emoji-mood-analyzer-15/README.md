# nightly-emoji-mood-analyzer

## Overview

`nightly-emoji-mood-analyzer` is a tiny Node.js command‑line utility that reads plain‑text from **STDIN** (or a file) and prints a single emoji representing the overall mood of the text. It uses a handcrafted list of positive and negative words, making it fast, offline, and dependency‑free.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install (no external deps)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-analyzer
npm install   # only creates a package‑lock, no packages are fetched
```

## Usage

```bash
# Pipe text into the CLI
echo "I love sunny days and fresh coffee!" | node src/index.js
# => 😊

# Or pass a file path as the first argument
node src/index.js ./sample.txt
```

## How it works

The script tokenises the input, counts how many words appear in a small positive‑word list versus a negative‑word list, and selects an emoji based on the net score:

* **Positive score** → 😊 (smiling face)
* **Negative score** → 😞 (disappointed face)
* **Neutral or no sentiment words** → 😐 (neutral face)

## Testing

Run the bundled tests with:

```bash
npm test
```

The test suite lives in `tests/` and uses Node's built‑in `assert` module.

## License

MIT © ApocalypsAI community
