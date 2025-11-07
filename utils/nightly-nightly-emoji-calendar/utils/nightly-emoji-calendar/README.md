# Nightly Emoji Calendar

A lightweight, zero‑dependency Python utility that prints a month calendar where each day is represented by a fun emoji:

- **🌞** – regular weekday
- **🌙** – weekend (Saturday & Sunday)
- **🎉**, **🎄**, **🦃**, … – mock holiday emojis (hard‑coded for demonstration)

## Features

- Stand‑alone CLI (`python -m src.emoji_calendar [YYYY-MM]`)
- Deterministic output for any month/year
- Offline‑friendly tests using simple mocks

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and run the CLI
python -m utils/nightly-emoji-calendar/src/emoji_calendar 2025-03
```

If no argument is supplied, the current month is used.

## Testing

```bash
python -m unittest discover utils/nightly-emoji-calendar/tests
```

The test suite mocks the holiday lookup to keep everything deterministic and offline.
