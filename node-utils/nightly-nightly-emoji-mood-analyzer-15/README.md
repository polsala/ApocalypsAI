# nightly-emoji-mood-analyzer

A tiny Node.js CLI utility that reads a short piece of text and outputs an emoji that best matches the mood. Whimsical, yet handy for adding a touch of emotion to logs, commit messages, or chat bots.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js "I am feeling great today!"
# => 😊
```

Or pipe input:

```sh
echo "I'm so sad..." | node src/index.js
# => 😢
```

## How it works

The tool looks for simple keyword lists for happy, sad, and angry moods. If none match, it returns a thinking face 🤔.

## Testing

```sh
npm test
```
