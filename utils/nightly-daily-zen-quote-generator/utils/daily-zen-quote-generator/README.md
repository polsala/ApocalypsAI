# Daily Zen Quote Generator

A whimsical yet useful CLI that prints a deterministic "quote of the day" from a built‑in collection. No network calls; works offline.

## Features

- Zero external dependencies beyond the Python standard library.
- Deterministic output based on the current date (or a supplied date).
- Handy for adding daily inspiration to scripts, terminals, or CI logs.

## Installation

Copy the `utils/daily-zen-quote-generator` folder into your project and run:

```sh
python -m utils.daily-zen-quote-generator.src.main
```

## Usage

```sh
# Print today's quote
python -m utils.daily-zen-quote-generator.src.main

# Print quote for a specific date (YYYY-MM-DD)
python -m utils.daily-zen-quote-generator.src.main --date 2023-04-01
```

## License

MIT
