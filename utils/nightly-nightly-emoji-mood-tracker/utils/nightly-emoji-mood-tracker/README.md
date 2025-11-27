# Nightly Emoji Mood Tracker

Utility that scans a text for emojis and reports an aggregated mood.

## Installation

```bash
pip install .
```

## Usage

```bash
python -m utils.nightly-emoji-mood-tracker.src.emoji_mood --text "I love 🍕 and 🎉!"
```

The command prints a human‑readable mood summary, e.g. `Very Happy`.

## How it works

* A small hard‑coded map assigns each supported emoji a numeric mood value.
* The utility extracts emojis present in the input text, sums their values, and translates the total into a textual mood category.
* No external services are called – everything runs offline.

## Supported emojis (partial list)

| Emoji | Mood value |
|-------|------------|
| 😀 😃 😄 😁 😂 🤣 😊 😍 🥰 🎉 👍 ❤️ | +1 |
| 😢 😭 😡 😠 👎 💔 💩 | -1 |

Feel free to extend the map in `src/emoji_mood.py`.
