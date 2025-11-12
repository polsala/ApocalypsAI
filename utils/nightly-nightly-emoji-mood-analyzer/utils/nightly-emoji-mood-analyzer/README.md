# Nightly Emoji Mood Analyzer

A tiny Python utility that scans a piece of text for emojis and reports the dominant mood.

## Features
- Detects four mood categories: **happy**, **sad**, **angry**, **love**.
- Simple CLI: `python -m src.emoji_mood <path-to-text-file>`
- Pure Python, no external dependencies.

## Usage

```bash
echo "I love this! 😍😍" > sample.txt
python -m src.emoji_mood sample.txt
# Output: love
```

## How it works
The script maps a set of emojis to mood buckets, counts occurrences, and returns the bucket with the highest count. Ties are broken by a predefined priority order.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
