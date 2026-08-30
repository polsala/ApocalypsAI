# nightly-emoji-crypt-decoder

A whimsical CLI that translates a string of emojis into a readable phrase using a built‑in apocalyptic dictionary.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/main.js 🌧️☢️
# => rain radiation
```

You can also pipe the output into other commands or use it in scripts.

## How it works

The tool contains a small dictionary of emojis commonly seen in post‑apocalyptic stories. Each emoji is replaced by its word; unknown emojis become “?”.

## License

MIT
