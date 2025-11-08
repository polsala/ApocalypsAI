# Daily Apocalypse Tip

Utility that prints a whimsical survival tip for the day. The tip is deterministic and derived from the current date, so the same date always yields the same tip.

## Usage

```bash
# Run the tip generator (prints today's tip)
python -m src.tip_generator

# Or specify a date (YYYY-MM-DD)
python -m src.tip_generator --date 2023-01-01
```

## How it works

The module contains a short list of tongue‑in‑cheek apocalypse survival tips. The tip for a given date is selected by:

```python
index = date.toordinal() % len(_TIPS)
```

Because `date.toordinal()` is stable, the output is repeatable and requires no network access.

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```
