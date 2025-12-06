# Whimsical Emoji Clock

A **stand‑alone** Python utility that converts a 24‑hour time (e.g., `14:30`) into a single emoji that captures the mood of that hour.

## Features
- No external dependencies – pure standard library.
- Works as a library function **and** a command‑line tool.
- Deterministic mapping:
  - **00:00‑05:59** → 🌙 (night)
  - **06:00‑11:59** → 🌅 (sunrise)
  - **12:00‑17:59** → ☀️ (day)
  - **18:00‑23:59** → 🌇 (sunset)

## Installation
```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv && source .venv/bin/activate
pip install -e utils/whimsical-emoji-clock
```

## Usage
```bash
# As a library
>>> from emoji_clock import get_emoji_for_time
>>> get_emoji_for_time("07:45")
'🌅'

# As a CLI
$ python -m emoji_clock 21:15
🌇
```

## Testing
```bash
pytest utils/whimsical-emoji-clock/tests
```

All tests are offline and deterministic.
