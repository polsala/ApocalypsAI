# nightly-emoji-mood-tracker

## Overview

`nightly-emoji-mood-tracker` creates a **deterministic** list of emojis representing a “mood” for each day in a supplied date range. The mapping is based on a SHA‑256 hash of the ISO‑formatted date, so the same date always yields the same emoji without any network calls.

## Features

- Pure Python 3.11, no external dependencies.
- Deterministic output – perfect for reproducible scripts and offline use.
- Small CLI (`python -m nightly-emoji-mood-tracker`) and importable API.
- Includes a full test suite that runs offline using mocks.

## Installation

Copy the `utils/nightly-emoji-mood-tracker` folder into your project and add it to your `PYTHONPATH` or install it as a package if you wish.

```bash
# From the repository root
pip install -e utils/nightly-emoji-mood-tracker
```

## Usage

### CLI

```bash
python -m nightly-emoji-mood-tracker --start 2023-01-01 --end 2023-01-07
```

Output:

```
2023-01-01: 😀
2023-01-02: 🤔
2023-01-03: 😎
2023-01-04: 🥳
2023-01-05: 😐
2023-01-06: 😔
2023-01-07: 🤩
```

### Library

```python
from nightly_emoji_mood_tracker.src.tracker import generate_mood_calendar

calendar = generate_mood_calendar("2023-01-01", "2023-01-07")
# calendar -> [("2023-01-01", "😀"), ("2023-01-02", "🤔"), ...]
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-mood-tracker/tests
```

The tests are deterministic and use mocks to avoid any external state.
