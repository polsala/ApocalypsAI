# Daily Zen Quote Generator

A tiny utility that prints a daily Zen‑style quote. The quote is deterministic: it depends only on the current date, so the same day always yields the same quote without any network calls.

## Features

- No external dependencies beyond the Python standard library.
- Offline‑friendly – all quotes are baked into the package.
- CLI: `python -m zen_quote` prints today’s quote.
- Library function `get_quote(date: datetime.date | None = None) -> str`.

## Usage

```bash
$ python -m zen_quote
🧘 Today’s Zen: “The obstacle is the path.”
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
