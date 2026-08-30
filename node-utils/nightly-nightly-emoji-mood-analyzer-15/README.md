# nightly-emoji-mood-analyzer

Analyzes a piece of text and outputs an emoji that best represents the overall mood.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js "I am so happy and excited!"
# => 😄
```

You can also pipe text via stdin:

```sh
echo "I am angry and upset." | node src/index.js
# => 😠
```

## How it works

The tool looks for keywords associated with four moods: happy, sad, angry, and neutral. The mood with the most matches wins. If no keywords are found, it returns the neutral emoji 🤔.
