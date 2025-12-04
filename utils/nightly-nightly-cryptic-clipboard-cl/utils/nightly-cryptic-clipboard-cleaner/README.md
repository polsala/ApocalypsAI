# Nightly Cryptic Clipboard Cleaner

Utility to sanitize clipboard text: removes non‑ASCII characters, normalizes whitespace, and preserves basic punctuation (e.g., dashes). Handy for preparing text before pasting into code or a terminal.

## Usage

```bash
# Pipe text into the utility
echo "Hello World! " | python -m src.clipboard_cleaner
# Output: Hello World!
```

Or import in Python:

```python
from src.clipboard_cleaner import clean_clipboard
cleaned = clean_clipboard("Some text ")
print(cleaned)  # -> "Some text"
```

## Installation

Just run the script; no external dependencies beyond the Python standard library.
