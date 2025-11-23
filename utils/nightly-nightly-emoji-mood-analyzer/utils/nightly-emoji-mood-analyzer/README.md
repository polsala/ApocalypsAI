# Nightly Emoji Mood Analyzer

A whimsical yet practical utility that scans a short piece of text and returns an emoji reflecting its sentiment:

- **Positive** → `😊`
- **Neutral**  → `😐`
- **Negative** → `😞`

## Features

- **Zero external dependencies** – pure Python 3.11.
- **Deterministic** – uses simple keyword matching, no randomness.
- **CLI** – `python -m utils/nightly-emoji-mood-analyzer/src/emoji_mood "Your text here"`.
- **Tested** – unit tests cover positive, negative, neutral, case‑insensitivity and tie‑breakers.

## Installation & Usage

The utility is self‑contained; just copy the folder into the repository and run the module:

```bash
python -m utils/nightly-emoji-mood-analyzer/src/emoji_mood "I love this!"
# → 😊
```

## How It Works

A tiny word‑list based sentiment scorer counts occurrences of known positive and negative words (case‑insensitive). The emoji with the higher count is returned; ties default to neutral.

## License

MIT – see the repository root LICENSE file.
