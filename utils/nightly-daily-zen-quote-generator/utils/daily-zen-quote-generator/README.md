# Daily Zen Quote Generator

Utility that returns a deterministic "quote of the day" from a curated list of Zen sayings. No network calls; works offline. Perfect for adding a touch of calm to scripts, CI logs, or terminal prompts.

## Usage

```sh
python -m daily_zen_quote_generator
# or
python src/main.py
```

Outputs a single line quote.

## How it works

The quote is selected by hashing the current date (YYYY‑MM‑DD) and mapping it to an index in the built‑in list. The same date always yields the same quote.

## Testing

Run `pytest` in the `tests/` directory.
