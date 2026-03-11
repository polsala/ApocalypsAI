# nightly-emoji-mood-analyzer

A whimsical CLI tool that scans a piece of text and returns an emoji representing its overall mood. Useful for quickly gauging sentiment in logs, notes, or chat messages.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js "I love sunny days!"
# 😊

node src/index.js < input.txt
# 😢
```

## How it works

The tool uses a simple keyword‑based sentiment analysis. It looks for positive words (joy, love, happy, etc.) and negative words (sad, angry, hate, etc.) and returns an appropriate emoji.

## License

MIT
