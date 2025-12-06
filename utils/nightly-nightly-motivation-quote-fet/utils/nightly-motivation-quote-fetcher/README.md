# Nightly Motivation Quote Fetcher

## Overview

`nightly-motivation-quote-fetcher` provides a single function `get_random_quote()` that returns a random motivational quote from an internal collection. The utility is completely offline, has no external dependencies beyond the Python standard library, and includes a deterministic test suite.

## Usage

```python
from quote_fetcher import get_random_quote

print(get_random_quote())
```

Running the script will print a random quote each time. The utility can be imported into other projects or invoked from a CI step to add a cheerful message to logs or pull‑request comments.

## Files

- `src/quote_fetcher.py` – implementation
- `tests/test_quote_fetcher.py` – deterministic unit tests using `unittest.mock`

## License

MIT © ApocalypsAI
