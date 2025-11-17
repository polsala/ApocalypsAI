# nightly-zen-quote-of-the-day

**What it does**

A tiny, self‑contained utility that prints a Zen‑style quote that changes every day. The quote is deterministic – it is derived from the calendar date, so every run on the same day yields the same output without any network calls.

**Why it’s useful**

- Gives a pleasant, low‑noise daily reminder in CI logs, terminal prompts, or Slack bots.
- No external dependencies, works offline.
- Deterministic selection makes testing trivial.

**Installation**

The utility lives under `utils/nightly-zen-quote-of-the-day/`. It can be executed directly with Python:

```bash
python -m utils.nightly-zen-quote-of-the-day.src.quote
```

Or imported in your own scripts:

```python
from utils.nightly-zen-quote-of-the-day.src.quote import get_quote
print(get_quote())
```

**How it works**

1. A short list of Zen‑inspired quotes is baked into the source.
2. The current date (or a supplied `datetime.date`) is converted to its ordinal number.
3. The ordinal modulo the number of quotes selects the quote for that day.

**Testing**

Run the bundled tests with `pytest`:

```bash
pytest utils/nightly-zen-quote-of-the-day/tests
```
