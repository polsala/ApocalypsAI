# Nightly Motivation Quote

A tiny utility that returns a deterministic "Quote of the Day" from a curated list of inspirational sayings.  
The quote is selected based on the current date (or a supplied date) using a simple ordinal‑based algorithm, making it completely offline and reproducible.

## Usage

```python
from src.quote import get_quote_of_the_day

print(get_quote_of_the_day())          # today's quote
print(get_quote_of_the_day(date=date(2023, 1, 1)))  # specific date
```

## Why?

- Perfect for terminal greetings, daily stand‑up messages, or CI logs.
- No network calls, no dependencies beyond the Python standard library.
- Deterministic: the same date always yields the same quote.
