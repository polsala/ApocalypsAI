# Daily Emoji Generator

A whimsical yet useful utility that prints a random emoji from a curated list.

## Features
- Zero external dependencies (standard library only).
- Deterministic mode via an optional seed – ideal for testing.
- Simple CLI: `python -m src.emoji_generator` prints an emoji.
- Importable function `get_random_emoji(seed: int | None = None) -> str`.

## Usage
```bash
# Random emoji
python -m src.emoji_generator

# Deterministic emoji (seed = 42)
python -m src.emoji_generator --seed 42
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
