# nightly-emoji-mood-analyzer

A tiny Node.js utility that evaluates a short piece of text and returns an emoji reflecting its mood (ð, ð¢, ð , ð¤). Useful for adding emotional flair to logs, commit messages, or chat bots.

## Installation

```sh
npm install -g nightly-emoji-mood-analyzer
```

## Usage

```sh
npx nightly-emoji-mood-analyzer "I love the new features!"
# => ð
```

Or pipe input:

```sh
echo "The build failed again." | npx nightly-emoji-mood-analyzer
# => ð 
```

## How it works

The tool uses a simple wordâlist sentiment analysis: it counts occurrences of positive and negative keywords. If positives outweigh negatives, it returns a happy emoji; if negatives outweigh positives, an angry emoji; otherwise a neutral thinking emoji.

## Testing

```sh
npm test
```
