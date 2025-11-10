# Daily Zen Quote Dispenser

A whimsical yet practical utility that provides a random Zen‑style quote. Perfect for adding a moment of calm to your terminal, CI logs, or daily stand‑ups.

## Features

- **Random quote** from a curated list of Zen sayings.
- Optional **length filter** to keep quotes short enough for commit messages or status lines.
- Simple **CLI** (`python -m daily_zen_quote_dispenser`) that prints a quote to stdout.
- Fully **self‑contained** – no external API calls, works offline.

## Installation

Copy the `utils/daily-zen-quote-dispenser` folder into your repository and add it to your Python path, or install it as a module:

```bash
pip install -e utils/daily-zen-quote-dispenser
```

## Usage

```bash
# Print a random quote
python -m daily_zen_quote_dispenser

# Print a short quote (≤ 60 characters)
python -m daily_zen_quote_dispenser --max-length 60
```

## API

```python
from daily_zen_quote_dispenser import get_zen_quote

quote = get_zen_quote()               # any random quote
short_quote = get_zen_quote(max_length=80)  # quote ≤ 80 chars
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/daily-zen-quote-dispenser/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
