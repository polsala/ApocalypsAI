# nightly-emoji-mood-analyzer

A whimsical CLI that turns a line of text into an emoji reflecting its mood.

## Installation

```sh
npm install -g .
```

## Usage

```sh
echo "I love sunny days!" | nemoji
# => 😊
```

Or:

```sh
nemoji "I am feeling gloomy."
# => 😔
```

## How it works

Uses a tiny built‑in word list to score positivity vs negativity and maps the result to an emoji.

## License

MIT
