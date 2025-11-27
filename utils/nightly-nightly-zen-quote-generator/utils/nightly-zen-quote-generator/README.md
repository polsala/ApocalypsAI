# Nightly Zen Quote Generator

A tiny, self‑contained utility that serves a random Zen‑style quote.  It can optionally filter quotes by a tag (e.g., `mindfulness`, `humor`).

## Features
- Built‑in list of 12 curated quotes – no network access required.
- Simple Python API: `get_random_quote(tag=None)`.
- Command‑line interface:
  ```bash
  python -m zen_quote [--tag TAG]
  ```
- Deterministic unit tests using `unittest.mock`.

## Usage
```python
from zen_quote import get_random_quote

quote = get_random_quote()               # any random quote
quote = get_random_quote(tag="humor")   # only humor‑tagged quotes
print(f"\"{quote['text']}\" — {quote['author']}")
```

## Installation
The utility is pure Python 3.11 and has **no external dependencies**.  Copy the `src/` folder into your project or run it directly from the repository.
