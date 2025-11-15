# Daily Zen Quote Generator

A tiny Python utility that prints a deterministic "Zen" quote for the current day. The quote changes each day but is reproducible, making it safe for offline use and testing.

## Features

- No external dependencies.
- Deterministic selection based on the date (no randomness).
- Simple CLI: `python -m zen_quote` prints today's quote.
- Easy to embed in scripts or CI pipelines for a daily dose of mindfulness.

## Usage

```bash
python -m zen_quote
# → “The journey of a thousand miles begins with one step.”
```

## Implementation Details

- Quotes are stored in a hard‑coded list.
- The index is computed as `hash(date.isoformat()) % len(quotes)`.
- The hash is taken from Python's built‑in `hash()` after normalising the seed with `hash(date_str) & 0xffffffff` to make it stable across runs.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
