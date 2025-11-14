# Daily Zen Quote Generator

Utility that returns a deterministic "quote of the day" from a curated list. No network calls; works offline. Ideal for adding a splash of inspiration to scripts, CI pipelines, or terminal prompts.

## Usage

```bash
python -m daily_zen_quote_generator
# or
python src/main.py
```

Outputs a single line quote.

## How it works

The quote is selected by taking the current UTC date, converting it to an integer (YYYYMMDD) and using modulo arithmetic against the number of quotes in the bundled `quotes.json`.

## Testing

Run:

```bash
python -m unittest discover -s tests
```
