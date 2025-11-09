# Daily Zen Quote Generator

A whimsical yet practical utility that prints a random Zen‑style quote to the console.

## Features

- **Zero external dependencies** – all quotes are bundled in the package.
- **CLI**: `python -m zen_quote [--max-length N]`
- **Length filter**: optionally limit the quote length.
- **Deterministic tests** using `unittest.mock`.

## Installation & Usage

```bash
# From the repository root
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install .

# Print a random quote
python -m zen_quote

# Only quotes <= 80 characters
python -m zen_quote --max-length 80
```

## Development

Run the test suite with:

```bash
pytest -q
```

## License

MIT – see the top‑level LICENSE file.
