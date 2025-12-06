# Nightly Cryptic Quote Dispenser

`nightly-cryptic-quote-dispenser` is a tiny, self‑contained utility that prints a random, apocalypse‑flavored quote. It can be used in CI logs, commit messages, or just for a daily dose of drama.

## Features
- No external dependencies – everything lives in the source tree.
- Deterministic output for testing via an optional seed.
- Simple CLI (`python -m src.quote_dispenser`).

## Usage
```bash
# Run the CLI
python -m utils.nightly-cryptic-quote-dispenser.src.quote_dispenser

# Use as a library
from utils.nightly-cryptic-quote-dispenser.src.quote_dispenser import get_random_quote
print(get_random_quote())
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/nightly-cryptic-quote-dispenser/tests
```
