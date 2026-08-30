# nightly-emoji-mood-analyzer

A whimsical CLI utility that analyzes a short piece of text and returns an emoji representing the overall mood. Uses simple keyword matching.

## Installation

```sh
# No installation needed, just run with Node.js
```

## Usage

```sh
node src/index.js "I am feeling great today!"
# => 😊
```

## How it works

The tool scans the input for keywords associated with common emotions and returns a corresponding emoji. If no keywords are found, it returns a thinking face 🤔.

## Testing

```sh
node tests/test_index.js
```
