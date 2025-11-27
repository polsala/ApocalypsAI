# Daily Zen Quote Generator

A whimsical yet practical utility that prints a random Zen‑inspired quote from a built‑in collection.

## Features

- No network access – all quotes are bundled.
- Simple CLI: `python -m daily_zen_quote_generator` prints a quote.
- Easy to embed in scripts, CI pipelines, or terminal prompts.

## Usage

```sh
$ python -m daily_zen_quote_generator
The journey of a thousand miles begins with one step.
```

## Installation

Copy the `utils/daily-zen-quote-generator` folder into your project and run the script with Python 3.11 or later.

## Testing

```sh
$ python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
