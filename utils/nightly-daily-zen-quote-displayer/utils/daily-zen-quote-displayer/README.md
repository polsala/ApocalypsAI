# Daily Zen Quote Displayer

A tiny utility that prints a deterministic "Zen" quote for the current day. Optionally filter by theme (e.g., "mindfulness", "nature").

## Features

- **No network access** – quotes are baked into the package.
- **Deterministic output per day**, useful for reproducible scripts.
- Simple CLI: `python -m daily_zen_quote_displayer [--theme THEME]`.

## Usage

```bash
python -m daily_zen_quote_displayer
# or
python -m daily_zen_quote_displayer --theme mindfulness
```

## Installation

Copy the folder into your project and run with Python 3.11.

## Testing

```bash
pytest -q utils/daily-zen-quote-displayer/tests
```
