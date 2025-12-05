# nightly-emoji-stats

## Overview

`nightly-emoji-stats` is a lightweight, zero‑dependency Python utility that reads a text file and reports how many times each emoji appears. It prints the result as a JSON object sorted by descending count.

## Usage

```bash
python -m src.emoji_stats <path-to-text-file>
```

The script will output something like:

```json
{"😀": 3, "🚀": 1, "❤️": 2}
```

## How it works

* Reads the entire file as UTF‑8 text.
* Uses a regular expression that matches the Unicode emoji ranges defined by the `emoji` specification.
* Tallies occurrences in a `collections.Counter` and prints a JSON‑encoded dictionary.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```

The tests are deterministic and use in‑memory mocks, so they work offline.
