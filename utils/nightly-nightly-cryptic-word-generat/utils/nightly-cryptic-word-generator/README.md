# Nightly Cryptic Word Generator

Utility that picks a random cryptic word from a curated list and shows its definition. Great for daily inspiration or puzzles.

## Usage

```bash
python -m utils.nightly-cryptic-word-generator.src.cryptic_word
```

Will print JSON like `{"word": "obfuscate", "definition": "make obscure"}`.

## API

`get_random_word() -> dict` returns a dict with keys `word` and `definition`.
