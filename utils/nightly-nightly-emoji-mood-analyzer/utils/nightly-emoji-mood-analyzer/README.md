# Emoji Mood Analyzer

## Overview

`nightly-emoji-mood-analyzer` is a whimsical yet practical command‑line utility that inspects a piece of text, determines its overall sentiment, and prints a matching emoji.  It can be used to quickly add emotional flair to commit messages, chat snippets, or any short prose.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- Deterministic, rule‑based sentiment analysis (positive, negative, neutral).
- Simple CLI: `python -m src.analyzer "Your text here"`.
- Programmatic API via `analyze_mood(text: str) -> dict`.

## Installation

The utility lives under the repository’s `utils/` folder, so no installation step is required.  From the repository root you can run:

```bash
python -m utils/nightly-emoji-mood-analyzer/src/analyzer "I love sunny days!"
```

## Usage

```text
$ python -m utils/nightly-emoji-mood-analyzer/src/analyzer "I love sunny days!"
😊 (positive)
```

## Development & Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-mood-analyzer/tests
```

The tests are deterministic and offline – they rely only on the built‑in word lists.
