# Nightly Emoji Mood Analyzer

A tiny, self‑contained Python utility that reads a line of text and outputs an emoji reflecting its sentiment.

## Features
- **Zero dependencies** – pure Python 3.11 standard library.
- Simple rule‑based sentiment analysis using curated word lists.
- CLI entry point for quick use in scripts or GitHub Actions.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-mood-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m src.emoji_mood_analyzer "I love this new feature!"
# → 😊
```

## Testing
```bash
pytest -q
```

## License
MIT © ApocalypsAI
