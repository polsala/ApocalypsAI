# Emoji Mood Analyzer

Utility that scans a text file and reports the most frequent emoji(s) found. Helpful for summarizing mood in chat logs, comments, or any Unicode text.

## Usage

```bash
python -m utils.nightly-emoji-mood-analyzer.src.analyzer <path-to-text-file>
```

The command prints a JSON object with two keys:

- `most_common`: a list of the emoji(s) that appear the most times.
- `counts`: a mapping from each of those emoji to its occurrence count.

## How it works

1. Reads the file as UTF‑8.
2. Uses a regular expression that covers the most common emoji Unicode blocks.
3. Counts occurrences with `collections.Counter`.
4. Returns the emoji(s) with the highest count.

## Tests

Run the test suite with **pytest**:

```bash
pytest utils/nightly-emoji-mood-analyzer/tests
```

The tests are deterministic and run offline.
