# Daily Zen Quote Displayer

`daily-zen-quote-displayer` is a lightweight, zero‑dependency Python utility that prints a random Zen‑style quote each time it runs. It can be used directly from the command line, imported as a module, or invoked from CI pipelines to sprinkle a bit of calm into noisy logs.

## Features
- Bundled collection of 10+ curated Zen quotes.
- Deterministic output when a seed is supplied (useful for testing).
- Pure‑Python, works on any platform with Python 3.11+.
- No external network calls – fully offline.

## Installation
```bash
# From the repository root
pip install ./utils/daily-zen-quote-displayer
```

## Usage
```bash
# Print a random quote
python -m daily_zen_quote_displayer

# Print a deterministic quote (useful for scripts)
python -m daily_zen_quote_displayer --seed 42
```

## Development
Run the test suite with:
```bash
pytest utils/daily-zen-quote-displayer/tests
```
