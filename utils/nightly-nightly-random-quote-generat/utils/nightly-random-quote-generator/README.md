# Nightly Random Quote Generator

Utility that returns a whimsical quote from a curated list. Supports optional tag filtering and output formats (plain text or JSON). No external dependencies.

## Features
- Random quote selection from an internal list.
- Filter quotes by tag (e.g., `humor`, `inspiration`).
- Output as plain text or JSON.
- Fully self‑contained; works with the standard library only.

## Usage
```bash
python -m src.quote_generator [--tag <tag>] [--format text|json]
```

### Examples
```bash
# Any random quote
python -m src.quote_generator

# Only inspirational quotes, JSON output
python -m src.quote_generator --tag inspiration --format json
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s tests
```
