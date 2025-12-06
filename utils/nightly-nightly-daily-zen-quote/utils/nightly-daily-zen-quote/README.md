# Daily Zen Quote

Utility that returns a deterministic "Zen" quote for any given date. Useful for adding a daily inspirational line to scripts, terminals, or CI logs. The quote changes each day but is reproducible (same date → same quote).

## Usage

```bash
python -m utils.nightly-daily-zen-quote.src.zen_quote
# or
python utils/nightly-daily-zen-quote/src/zen_quote.py
```

Will print today's quote.

You can also import the function:

```python
from utils.nightly-daily-zen-quote.src.zen_quote import get_zen_quote
quote = get_zen_quote()  # today's quote
```

## How it works

A static list of quotes is indexed by the ordinal of the date modulo the number of quotes, ensuring the same date always yields the same quote.
