# Daily Zen Quote Generator

A whimsical yet useful utility that returns a random Zen‑inspired quote.  
All quotes are stored locally, so the tool works offline and requires no external dependencies.

## Features

- `get_quote(theme=None)`: Python function returning a random quote.
- CLI: `python -m src.main [--theme <theme>]` prints a quote to stdout.
- Themes such as `journey`, `mind`, `simplicity`, `growth`, `silence` are supported.

## Installation

Copy the folder `utils/daily-zen-quote-generator` into your project and run:

```bash
python -m src.main
```

or import the function:

```python
from src.main import get_quote
print(get_quote())
```

## Testing

```bash
python -m unittest discover -s tests
```

The tests mock randomness to stay deterministic and offline.
