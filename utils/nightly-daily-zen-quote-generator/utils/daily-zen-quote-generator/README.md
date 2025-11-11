# Daily Zen Quote Generator

A tiny utility that prints a random Zen‑style quote. Useful for adding a moment of calm to scripts, terminals, or CI logs.

## Features

- Built‑in list of 10+ quotes (no external API)
- Optional `--max-length` to restrict quote length
- Simple CLI: `python -m daily_zen_quote_generator` (or `python src/quote_generator.py`)
- Fully offline, deterministic tests using mocks.

## Usage

```sh
python -m daily_zen_quote_generator
# or
python src/quote_generator.py
```

Optional length:

```sh
python src/quote_generator.py --max-length 50
```

## License

MIT
