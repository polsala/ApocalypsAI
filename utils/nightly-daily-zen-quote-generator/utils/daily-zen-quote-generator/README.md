# Daily Zen Quote Generator

Utility that prints a random Zen‑inspired quote.  It can be used directly from the command line or imported as a Python module.

## Features
- No external dependencies – everything lives in the repository.
- Deterministic output for testing via an optional `seed` argument.
- Simple CLI (`python -m utils.daily-zen-quote-generator.src.main`).

## Usage
```bash
# Run the CLI
python -m utils.daily-zen-quote-generator.src.main
```

Or from Python:
```python
from utils.daily-zen-quote-generator.src.main import get_quote

print(get_quote())          # random quote
print(get_quote(seed=42))   # deterministic quote for the given seed
```

## Testing
```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
