# Emoji Mood Analyzer

Utility that reads a text file and outputs a histogram of emojis representing the overall mood of the text. Works offline, no external APIs.

## How it works

- Scans the text for predefined keyword lists for happy, sad, angry, neutral.
- Counts occurrences and maps them to emojis:
  - 😊 happy
  - 😢 sad
  - 😠 angry
  - 😐 neutral
- Prints a sorted list of emoji counts.

## Usage

```sh
python -m src.mood_analyzer path/to/file.txt
```

## Example

Input: `"I am happy but also a bit sad."`

Output:
```
😊: 1
😢: 1
😐: 0
😠: 0
```

## Tests

Run with `pytest`:

```sh
pytest -q
```
