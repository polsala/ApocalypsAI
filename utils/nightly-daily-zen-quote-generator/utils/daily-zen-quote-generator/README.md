# Daily Zen Quote Generator

Provides a simple Python utility that returns a deterministic "Zen" quote for each day of the year. The quote is selected from a built‑in list of 365 quotes (or repeats if fewer). Useful for adding a calming message to logs, CI pipelines, or personal scripts.

## Installation

Copy the folder into your repository. No external dependencies beyond the Python standard library.

## Usage

```bash
python -m daily_zen_quote_generator
# or
from quote_generator import get_quote
print(get_quote())
```

## API

`get_quote(date: datetime.date | None = None) -> str`

Returns the quote for the given date, or today if omitted.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
