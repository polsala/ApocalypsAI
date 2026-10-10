# nightly-emoji-mood-analyzer

A whimsical CLI tool that reads a short piece of text and returns an emoji representing the overall mood.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js "I love sunny days"
# => 😊
```

## How it works

The tool uses a tiny built‑in word list to score positivity, negativity, anger and surprise. The category with the highest score determines the emoji.

Supported emojis:
- 😊 Happy
- 😢 Sad
- 😠 Angry
- 😲 Surprised
- 😐 Neutral (default)

## Testing

```sh
npm test
```
