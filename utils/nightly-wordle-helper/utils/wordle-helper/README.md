# Wordle Helper

Utility to filter possible Wordle solutions based on a known pattern and a set of excluded letters.

## Features
- Pure‑Python, no external dependencies.
- Works offline with a built‑in list of common 5‑letter words.
- Simple API: `filter_words(pattern, excluded)`.

## Usage Example
```python
from src.wordle_helper import filter_words

# Known pattern: first letter 'a', fourth letter 'l', fifth letter 'e'
# Unknown positions are marked with '?' (or '_' )
possible = filter_words('a??le', excluded='')
print(possible)  # → ['apple']
```

## Pattern Syntax
- Exactly 5 characters long.
- Use `?` or `_` for unknown letters.
- All other characters are treated as known letters (case‑insensitive).

## Excluded Letters
Provide a string of letters that must **not** appear anywhere in the candidate word.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/wordle-helper/tests
```
