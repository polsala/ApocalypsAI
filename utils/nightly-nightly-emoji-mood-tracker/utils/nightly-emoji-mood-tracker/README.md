# Nightly Emoji Mood Tracker

## Overview

`nightly-emoji-mood-tracker` is a lightweight, zero‑dependency Python utility that analyses a short piece of text and returns a single emoji representing the overall mood.

It uses a deterministic keyword‑based heuristic, making it fast, offline, and fully testable.

## Installation

```bash
# From the repository root
cd utils/nightly-emoji-mood-tracker
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
python -m src.emoji_tracker "I am feeling great today!"
# → 😊
```

Or import it in your own code:

```python
from src.emoji_tracker import get_mood_emoji

emoji = get_mood_emoji("I am sad and lonely.")
print(emoji)  # 😢
```

## How it works

The script scans the input for predefined keyword groups (happy, sad, angry, love, fear). The group with the most matches determines the emoji. Ties fall back to a neutral face.

## Testing

```bash
pytest -q
```

All tests run offline and are deterministic.
