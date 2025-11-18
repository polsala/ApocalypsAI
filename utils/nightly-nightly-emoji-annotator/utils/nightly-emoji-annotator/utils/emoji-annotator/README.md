# Emoji Annotator

**Utility name:** `emoji-annotator`

## Overview

`emoji-annotator` scans a piece of text and appends an appropriate emoji after each recognised keyword. The mapping is deterministic and fully offline, making the tool safe for any environment.

## Features

- **Deterministic** – a static keyword‑to‑emoji map.
- **Case‑insensitive** whole‑word matching.
- **CLI** – annotate a file and print the result to stdout.
- **Library** – import `annotate_text` in your own Python code.

## Installation

The utility is self‑contained; just copy the `src/annotator.py` file and run it with Python 3.11.

```bash
python -m emoji_annotator path/to/file.txt
```

## Example

```text
Input:  I love fire and rocket.
Output: I love❤️ fire🔥 and rocket🚀.
```

## Testing

Run the bundled tests with `pytest`:

```bash
cd utils/nightly-emoji-annotator/utils/emoji-annotator
pytest -q
```
