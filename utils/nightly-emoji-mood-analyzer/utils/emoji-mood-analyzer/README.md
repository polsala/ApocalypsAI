# Emoji Mood Analyzer

A whimsical yet practical utility that reads a line of text and returns an emoji representing its overall mood. It uses a lightweight keyword‑based sentiment dictionary, so it works offline with zero dependencies beyond the Python standard library.

## Installation

Copy the `src/emoji_mood.py` file into your project or run it directly:

```bash
python -m utils.emoji-mood-analyzer.src.emoji_mood "I love sunny days!"
```

## Usage

```bash
python -m utils.emoji-mood-analyzer.src.emoji_mood "Your text here"
```

The script prints a single emoji, e.g. `😊`.

## How it works

The script maintains three small word lists:

- **Positive** words → 😊
- **Negative** words → 😞
- **Neutral** fallback → 😐

The sentiment score is the count of positive matches minus negative matches. A positive score yields a happy emoji, a negative score yields a sad emoji, and a zero score yields a neutral emoji.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/emoji-mood-analyzer/tests
```
