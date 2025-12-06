# Daily Quote Generator

Utility that returns a random quote from a built‑in collection.  It works completely offline and can optionally filter quotes by category (e.g., *motivation*, *humor*).  Perfect for adding a splash of inspiration to scripts, CI logs, or terminal sessions.

## Usage
```bash
python -m daily_quote_generator [category]
```
- `category` (optional): one of `motivation`, `humor`, or any other defined category.  If omitted or unknown, a quote is chosen from the full pool.

## Structure
- `src/quote.py` – core implementation.
- `tests/test_quote.py` – deterministic unit tests using mocks.
