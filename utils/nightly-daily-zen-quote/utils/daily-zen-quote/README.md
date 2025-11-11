# Daily Zen Quote

Utility that prints a deterministic "zen" quote for the current day. No network calls; uses a built‑in list of quotes. Helpful for adding a daily inspirational line to scripts, commit messages, or terminal prompts.

## Usage

```bash
python -m daily_zen_quote
```

Outputs a single line quote.

## How it works

- Takes today's date.
- Seeds a pseudo‑random generator with the ordinal of the date.
- Picks a quote from an internal list.

## Testing

Run:

```bash
python -m unittest discover -s utils/daily-zen-quote/tests
```
