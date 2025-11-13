# Daily Zen Quote Generator

A tiny, self‑contained utility that prints a random Zen‑style quote to the console.  It can optionally filter quotes by a *theme* (e.g., `mindfulness`, `nature`).

## Features
- No external network calls – quotes are baked into the package.
- Simple CLI: `python -m daily_zen_quote_generator [--theme THEME]`
- Deterministic unit tests using mocks.

## Usage
```bash
# Print any random Zen quote
python -m daily_zen_quote_generator

# Print a random quote about nature
python -m daily_zen_quote_generator --theme nature
```

## Structure
```
utils/daily-zen-quote-generator/
├─ README.md               # This file
├─ src/main.py             # Core implementation & CLI
└─ tests/test_main.py      # Deterministic offline tests
```
