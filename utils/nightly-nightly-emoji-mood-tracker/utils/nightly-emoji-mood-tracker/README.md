# Nightly Emoji Mood Tracker

A tiny CLI utility that converts a numeric mood score (‑10 to 10) into a single expressive emoji.

## Why?

Sometimes you just need a quick visual cue of how a day feels without writing a paragraph. Feed a score and get an emoji you can paste into chats, commit messages, or logs.

## Installation

The utility is self‑contained; just run the script with Python 3.11:

```bash
python -m utils/nightly-emoji-mood-tracker/src/emoji_mood.py <score>
```

## Usage

```bash
$ python -m utils/nightly-emoji-mood-tracker/src/emoji_mood.py 7
😄
```

Valid scores are integers from **‑10** (worst) to **10** (best). Out‑of‑range values produce an error.

## Development & Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-tracker/tests
```

The tests are deterministic and require no network access.

## Mapping

| Score Range | Emoji | Meaning |
|-------------|-------|---------|
| -10 … -7    | 😭    | Very sad |
| -6 … -3     | 😞    | Sad |
| -2 … 0      | 😐    | Neutral |
| 1 … 3       | 🙂    | Slightly happy |
| 4 … 7       | 😄    | Happy |
| 8 … 10      | 🤩    | Ecstatic |
