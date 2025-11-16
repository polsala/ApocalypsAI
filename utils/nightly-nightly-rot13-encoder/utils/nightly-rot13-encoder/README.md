# nightly‑rot13‑encoder

A whimsical yet practical utility that applies the classic ROT13 cipher to any text.

## Features
- **CLI**: `python -m src.rot13_encoder "Hello World"` prints the ROT13‑encoded string.
- **Library**: import `rot13` function from `src.rot13_encoder` for programmatic use.
- No external dependencies – pure Python 3.11.

## Usage
```bash
# Encode a string
python -m src.rot13_encoder "Apocalypse is coming"
# Decode (ROT13 is symmetric)
python -m src.rot13_encoder "Ncbcnpvrf vf pbzvat"
```

## Testing
Run the test suite with:
```bash
python -m unittest discover -s tests
```
