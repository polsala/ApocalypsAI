# Nightly Emoji Calendar

## Overview

`nightly-emoji-calendar` is a lightweight, self‑contained Python utility that prints the current date decorated with emojis that represent the **day of the week** and the **month**. It’s perfect for adding a splash of personality to daily logs, commit messages, or any place you want a quick, human‑readable timestamp.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic output** – given a `datetime.date` it always returns the same emoji string.
- **CLI friendly** – run `python -m src.calendar` to print today’s emoji‑date.
- **Tested** – includes offline unit tests that mock the current date.

## Usage

```bash
# From the utility root directory
python -m src.calendar
```

Typical output (for 2023‑10‑31, a Tuesday in October):

```
📅 Tue 🌰 Oct 31, 2023
```

## Emoji Mapping

| Weekday | Emoji |
|---------|-------|
| Monday    | 📅 |
| Tuesday   | 📅 |
| Wednesday | 📅 |
| Thursday  | 📅 |
| Friday    | 📅 |
| Saturday  | 📅 |
| Sunday    | 📅 |

| Month | Emoji |
|-------|-------|
| January   | ❄️ |
| February  | 🌹 |
| March     | 🍀 |
| April     | 🌷 |
| May       | 🌼 |
| June      | 🌞 |
| July      | 🏖️ |
| August    | 🌻 |
| September | 🍁 |
| October   | 🌰 |
| November  | 🍂 |
| December  | 🎄 |

## Development

The utility lives under `src/calendar.py`. The public function `get_emoji_date(date: datetime.date) -> str` can be imported and used programmatically.

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and use `unittest.mock` to replace `datetime.date.today`.
