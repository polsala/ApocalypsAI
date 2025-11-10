# Daily Zen Quote Generator

A tiny utility that returns a random Zen‑inspired quote from a built‑in collection. Useful for adding a splash of calm to scripts, terminals, or CI logs.

## Features

- `get_quote(tag=None)`: returns a random quote; optional tag filters (e.g., `mindfulness`, `humor`).
- Deterministic when `random.seed()` is set – perfect for testing.
- No external dependencies; pure Python 3.11.

## Usage

```bash
python -m daily_zen_quote_generator          # prints a random quote
python -m daily_zen_quote_generator --tag humor   # prints a humorous Zen quote
```

## Installation

Copy the folder into `utils/daily-zen-quote-generator` and run with Python 3.11.
