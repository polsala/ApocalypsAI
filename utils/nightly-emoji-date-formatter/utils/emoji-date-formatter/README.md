# Emoji Date Formatter

Utility that transforms an ISO‑format date (`YYYY‑MM‑DD`) into a whimsical emoji string. Useful for adding flair to logs, commit messages, or chat bots.

## Installation

```bash
pip install .
# or just copy the src folder
```

## Usage

```python
from formatter import date_to_emoji

print(date_to_emoji("2023-10-31"))
# → 2️⃣0️⃣2️⃣3️⃣ 🎃 3️⃣1️⃣
```

## How it works

- Year digits are mapped to their corresponding keycap number emojis.
- Month numbers are mapped to a themed emoji (see mapping table).
- Day digits are also keycap emojis.

## Tests

Run with `pytest`:

```bash
pytest -q
```
