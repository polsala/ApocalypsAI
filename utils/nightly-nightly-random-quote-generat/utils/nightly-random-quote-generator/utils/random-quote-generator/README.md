# Random Quote Generator

A lightweight, zero‑dependency Python utility that prints a random inspirational quote.

## Features
- Returns a random quote from a curated list.
- Optional `--keyword` flag to only consider quotes containing a given word (case‑insensitive).
- Simple CLI: `python -m random_quote_generator`.

## Usage
```bash
# Print any random quote
python -m random_quote_generator

# Filter by keyword (e.g., "dream")
python -m random_quote_generator --keyword dream
```

## Implementation
The utility lives in `src/generator.py` and exposes a `get_random_quote(keyword: str | None = None) -> str` function. The CLI wrapper uses `argparse` and prints the selected quote to stdout.

## Testing
The test suite (`tests/test_generator.py`) mocks `random.choice` to guarantee deterministic output. See the repository's CI workflow for automated test execution.
