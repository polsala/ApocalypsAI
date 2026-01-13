# Emoji Mood Analyzer

A whimsical yet useful commandâline utility that reads a short piece of text and returns an emoji representing its overall mood (positive, neutral, or negative).

## Install

```sh
npm install -g nightly-emoji-mood-analyzer
```

*(The package is not published; copy the source and run with `ts-node` or compile with `tsc`.)*

## Usage

```sh
emoji-mood "I love sunny days!"
# => ð
```

## How it works

The analyzer uses a tiny builtâin word list of positive and negative terms. It tokenises the input, counts matches, and decides:

- score > 0 â ð
- score < 0 â ð
- otherwise â ð

## Development

```sh
npm install
npm run build   # compiles TypeScript
npm test        # runs the bundled tests
```

## License

MIT
