# Daily Quote Rotator

Utility that returns a deterministic "daily quote" from a built‑in collection. The quote changes each day based on the calendar date, but the mapping is deterministic and requires no network access.

## Installation

```bash
# The utility is pure Python; copy the `src` folder into your project or install via pip if packaged.
```

## Usage

```bash
python -m src.quote_rotator          # prints today's quote
python -m src.quote_rotator 2023-01-01  # prints quote for a given date
```

## How it works

The utility stores a static list of quotes. The index is computed as:

```
index = (date.toordinal() + OFFSET) % len(QUOTES)
```

where `OFFSET` is a small constant to avoid starting at the first quote on the earliest possible date.

## Testing

Run the test suite with:

```bash
pytest -q
```
