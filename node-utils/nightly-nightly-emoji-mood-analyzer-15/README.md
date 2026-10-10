# nightly-emoji-mood-analyzer

A whimsical CLI tool that reads a text file and prints an emoji representing the overall mood of the text. Uses a tiny built‑in sentiment word list, works offline, and has no external dependencies.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js <path-to-text-file>
```

Outputs one of: 😊 😢 😐

## How it works

Counts occurrences of positive and negative words from a small dictionary. If positives > negatives → 😊, if negatives > positives → 😢, else 😐.

## Testing

```sh
npm test
```
