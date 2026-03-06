# nightly-emoji-mood-analyzer

A whimsical command‑line utility that reads a short piece of text and returns an emoji representing its overall mood.

## Installation

```sh
npm install -g .
# or
npm install
```

## Usage

```sh
node src/index.js "I am thrilled about the new adventure!"
# => 😊
```

Or after global install:

```sh
emoji-mood "I am feeling gloomy."
# => 😢
```

## How it works

It uses a tiny built‑in word list of positive and negative terms to compute a sentiment score and maps the result to one of four emojis:

- 😊 (positive)
- 😐 (neutral)
- 😢 (negative)
- 😡 (very negative)

## Testing

```sh
npm test
```
