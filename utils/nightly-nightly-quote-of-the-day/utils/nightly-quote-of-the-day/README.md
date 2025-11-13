# Nightly Quote of the Day

A whimsical utility that prints a random inspirational quote each time it runs. Optionally filter by tag (e.g., `--tag wisdom`). Great for adding a splash of motivation to terminal sessions, CI logs, or README banners.

## Installation

```bash
pip install .
# or just run the script directly:
python -m utils.nightly-quote-of-the-day.src.quote
```

## Usage

```bash
# Print any random quote
python -m utils.nightly-quote-of-the-day.src.quote

# Print a random quote tagged "wisdom"
python -m utils.nightly-quote-of-the-day.src.quote --tag wisdom
```

## Design

- No external data sources – quotes are baked into the package.
- Pure Python 3.11, no third‑party dependencies.
- Fully tested with deterministic offline tests.
