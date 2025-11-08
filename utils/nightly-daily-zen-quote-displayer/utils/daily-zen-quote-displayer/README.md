# Daily Zen Quote Displayer

Utility that prints a deterministic "quote of the day" from a curated list of Zen sayings. The quote changes each day but is reproducible (same date → same quote). Optionally filter by a theme (e.g., "mindfulness", "impermanence").

## Usage

```bash
python -m utils.daily-zen-quote-displayer.src.quote
```

Or, if you add the `src` directory to your `PYTHONPATH`:

```bash
python -m quote --theme mindfulness
```

## Options

- `--theme <theme>`: Limit the selection to quotes that contain the given tag (case‑insensitive). If omitted, any quote may be chosen.

## How it works

- Quotes are stored directly in the source file as a list of dictionaries.
- The current date (ISO format) seeds a `random.Random` instance, guaranteeing the same quote for a given day.
- Themes are matched against the `tags` field of each quote.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote-displayer/tests
```
