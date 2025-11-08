# Daily Zen Quote Generator

A tiny utility that returns a daily Zen quote. The quote changes each day based on the date, but is deterministic and requires **no network access**. Perfect for adding a calming message to scripts, terminal prompts, or CI logs.

## Usage

```bash
python -m src.quote
```

Will print today's quote.

Or import it in your own Python code:

```python
from src.quote import get_daily_quote
print(get_daily_quote())
```

## How it works

The utility ships with a built‑in list of Zen sayings. It selects a quote by taking the current date's ordinal value modulo the number of quotes, guaranteeing a repeatable daily rotation without any external dependencies.

## Testing

Run the test suite with:

```bash
pytest utils/daily-zen-quote-generator/tests
```

The tests mock the current date to ensure deterministic results.
