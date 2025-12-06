# Daily Quote Randomizer

A tiny offline utility that returns a random inspirational quote from a bundled collection.
It can optionally filter quotes by tag (e.g., "wisdom", "humor").

## Usage

```bash
python -m daily_quote_randomizer
```

Will print a random quote.

```python
from daily_quote_randomizer import get_random_quote

quote = get_random_quote()
print(f"{quote['text']} — {quote['author']}")
```

## Tags

Each quote may have one or more tags. Pass a tag to `get_random_quote(tag="wisdom")` to limit selection.

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```
