# Palindrome Checker

Utility to check if a string is a palindrome, ignoring case, spaces, and punctuation.

## Installation

Just ensure you have Python 3.11+ installed. No external dependencies.

## Usage

```bash
python -m palindrome_checker "A man, a plan, a canal: Panama"
```

Will output either:

- `✅ Palindrome!`
- `❌ Not a palindrome.`

You can also import the library:

```python
from palindrome import is_palindrome

print(is_palindrome("racecar"))  # True
```

## Testing

Run the bundled tests with:

```bash
pytest -q
```
