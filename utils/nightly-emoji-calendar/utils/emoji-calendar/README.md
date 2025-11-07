# Emoji Calendar

A tiny Python utility that turns a date string (`YYYY-MM-DD`) into a whimsical emoji representation. Useful for adding flair to logs, commit messages, or chat bots.

## Installation

```bash
# The utility is self‑contained; just copy the `src` folder or install as a package.
# No external dependencies are required.
```

## Usage

```python
from src.main import date_to_emoji

print(date_to_emoji("2023-10-31"))
# 🎃🗓️
```

## How it works

- The **year** is ignored – we focus on month and day.
- Each month maps to a themed emoji (e.g., 🎃 for October, 🎄 for December).
- Day numbers are split into individual digits and each digit is replaced with its emoji counterpart (0️⃣‑9️⃣).

## Testing

```bash
python -m unittest discover -s tests
```

The test suite runs offline and uses deterministic inputs.
