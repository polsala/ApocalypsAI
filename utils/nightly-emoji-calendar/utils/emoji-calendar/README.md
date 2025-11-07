# Emoji Calendar

`emoji-calendar` is a lightweight, zero‑dependency Python 3.11 utility that turns a calendar date into a fun emoji representation.

## Features
- Accepts an optional `--date YYYY-MM-DD` argument; defaults to the current local date.
- Maps weekdays, months, and day numbers to expressive emojis.
- Purely offline – no network calls, perfect for CI or GitHub Actions.

## Installation
```bash
# Clone the repository (or copy the folder) and run the script directly:
python -m utils.emoji-calendar.src.main [--date YYYY-MM-DD]
```

## Usage
```bash
# Today
python -m utils.emoji-calendar.src.main

# Specific date
python -m utils.emoji-calendar.src.main --date 2023-10-31
```

Typical output for `2023-10-31`:
```
🌜 🎃 3️⃣1️⃣
```

## Development
Run the test suite with:
```bash
python -m pytest utils/emoji-calendar/tests
```

---
*Created by the ApocalypsAI Nightly Integrator.*
