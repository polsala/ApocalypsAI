# nightly-emoji-mood-analyzer

A whimsical CLI utility that reads a piece of text and returns an emoji representing its overall mood. Useful for quickly gauging sentiment in logs, messages, or notes.

## Installation

```sh
npm install
```

## Usage

```sh
node src/index.js "I love sunny days but hate traffic"
# Output: 😊
```

Or pipe from a file:

```sh
cat diary.txt | node src/index.js
```

## How it works

The tool uses simple keyword matching to count happy, sad, and angry words and selects the dominant mood. If no mood‑related words are found, it returns a thinking face (🤔).
