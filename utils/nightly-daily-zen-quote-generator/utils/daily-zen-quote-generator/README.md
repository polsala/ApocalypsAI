# Daily Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑style quote each time you run it. The quotes are bundled with the package, so the tool works completely offline.

## Features

- **Zero external dependencies** – pure Python 3.11.
- **Deterministic tests** – uses mocks to avoid randomness and file‑system access.
- **CLI friendly** – run `python -m daily_zen_quote_generator` to get a quote.

## Usage

```bash
$ python -m daily_zen_quote_generator
"The journey of a thousand miles begins with a single step."
```

## Structure

```
utils/daily-zen-quote-generator/
├── README.md               # This file
├── src/
│   ├── quote_generator.py  # Core implementation
│   └── quotes.json          # Bundled quote list
└── tests/
    └── test_quote_generator.py  # Deterministic unit tests
```

## License

MIT – see the repository root LICENSE file.
