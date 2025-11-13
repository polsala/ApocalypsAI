# Daily Zen Quote Generator

Utility that returns a random Zen‑inspired quote. Can be used for daily motivation, commit messages, or as a tiny CLI tool.

## Usage

```bash
python -m daily_zen_quote_generator
```

Will print a random quote.

```python
from daily_zen_quote_generator import get_zen_quote
print(get_zen_quote())
```

Optionally filter by theme:

```python
print(get_zen_quote(theme="mindfulness"))
```

## Implementation

- Pure Python 3.11, no external dependencies.
- Quotes are stored in a built‑in list.
- Random selection uses `random.choice`.

## Tests

Run with `pytest`:

```bash
pytest -q
```
