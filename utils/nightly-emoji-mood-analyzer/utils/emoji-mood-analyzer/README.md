# Emoji Mood Analyzer

A whimsical yet handy CLI tool that reads a short piece of text and returns an emoji representing its overall mood. No external APIs; uses a simple keyword‑based heuristic.

## Installation

```bash
# Copy the `src` folder into your project or install as a package
pip install .
```

## Usage

```bash
python -m mood_analyzer "I love sunny days!"
# Output: 😊
```

## How it works

The analyzer scans the input for positive and negative keywords. If more positive words are found, it returns a happy emoji; if more negative, a sad emoji; otherwise a neutral face.

## Testing

```bash
pytest -q
```
