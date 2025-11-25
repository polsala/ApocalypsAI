# Nightly Emoji Mood Tracker

## Overview

`nightly-emoji-mood-tracker` is a lightweight, self‑contained Python utility that analyses a short piece of text and returns a single emoji representing the overall mood. It uses a deterministic keyword‑based heuristic, so it works offline with **no external dependencies** beyond the Python standard library.

## Features

- **Zero‑install**: just copy the folder and run the script.
- **Deterministic**: same input always yields the same emoji.
- **CLI friendly**: can read from a command‑line argument or STDIN.
- **Tested**: includes a small pytest suite with mocked inputs.

## Installation

```bash
# Clone the repository (or copy the folder) and navigate into it
cd utils/nightly-emoji-mood-tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, only stdlib used)
```

## Usage

```bash
# Pass a string as an argument
python -m src.emoji_mood "I am feeling great today!"
# → 😊

# Or pipe text via STDIN
echo "What a terrible day..." | python -m src.emoji_mood
# → 😢
```

## How it works

The script tokenises the input, counts occurrences of predefined *happy*, *sad*, and *angry* keywords, and selects the emoji with the highest count. If no keywords match or there is a tie, it falls back to a neutral face (😐).

## Testing

```bash
pytest -q
```

All tests run offline and use simple string fixtures; no network calls are performed.
