# Daily Zen Quote

`daily-zen-quote` is a lightweight, zero‑dependency Python utility that prints a random Zen‑inspired quote. It can be used directly from the command line or imported as a library.

## Features

- **Random quote** from a curated list of Zen sayings.
- **Deterministic mode** – provide an integer seed to get the same quote every time (perfect for CI logs or reproducible demos).
- Pure Python 3.11, no external packages.

## Installation

Copy the `utils/daily-zen-quote` folder into your project and add the `src` directory to your `PYTHONPATH` or install it as a package:

```bash
# From the repository root
python -m pip install -e utils/daily-zen-quote
```

## Usage

### As a CLI

```bash
python -m daily_zen_quote.src.quote          # random quote
python -m daily_zen_quote.src.quote --seed 42 # deterministic quote
```

### As a library

```python
from daily_zen_quote.src.quote import get_quote

print(get_quote())          # random
print(get_quote(seed=42))   # deterministic
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote/tests
```

---

*Happy quoting!*
