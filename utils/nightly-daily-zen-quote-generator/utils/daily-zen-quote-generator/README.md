# Daily Zen Quote Generator

Utility that prints a random Zen‑inspired quote.

## Features
- No external network calls – quotes are baked into the package.
- Simple CLI (`python -m daily_zen_quote_generator`) prints a quote.
- `get_zen_quote()` function can be imported and used in other Python code.

## Usage
```bash
# As a script
python -m daily_zen_quote_generator

# As a library
from daily_zen_quote_generator.src.main import get_zen_quote
print(get_zen_quote())
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
