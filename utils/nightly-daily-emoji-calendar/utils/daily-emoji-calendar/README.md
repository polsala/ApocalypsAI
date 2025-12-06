# Daily Emoji Calendar

A lightweight, zero‑dependency Python utility that prints a month calendar where weekends are represented by emojis (Saturday 🌞, Sunday 🌜). Perfect for adding a splash of fun to your terminal.

## Features
- Generates a human‑readable calendar for any year/month.
- Weekends are replaced with 🌞 (Saturday) and 🌜 (Sunday).
- Pure Python 3.11 standard library – no external packages.

## Installation
```bash
# Clone the repository (or copy the folder) and install the utility locally
cd utils/daily-emoji-calendar
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m daily_emoji_calendar <year> <month>
# Example:
python -m daily_emoji_calendar 2023 10
```

The command prints a calendar like:
```
      1  2 🌞 🌜
 5  6  7  8  9 🌞 🌜
12 13 14 15 16 🌞 🌜
19 20 21 22 23 🌞 🌜
26 27 28 29 30 🌞   
```

## Development
Run the test suite with:
```bash
pytest
```

## License
MIT © ApocalypsAI
