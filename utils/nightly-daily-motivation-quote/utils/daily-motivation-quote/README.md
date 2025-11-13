# Daily Motivation Quote

A whimsical yet useful command‑line utility that serves you a motivational quote.

## Features

- **Random quote**: `daily-motivation-quote` prints a random quote from a curated list.
- **Quote of the day**: `daily-motivation-quote --today` selects a deterministic quote based on the current date.
- **Length filter**: `--max-length <n>` limits the output to quotes with `n` characters or fewer.

## Installation

The utility is self‑contained and requires only Python 3.11 (no external dependencies).

```bash
# Clone the repository (or copy the folder) and add it to your PATH
cd utils/daily-motivation-quote
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Random quote
daily-motivation-quote

# Quote of the day (deterministic per calendar day)
 daily-motivation-quote --today

# Random quote limited to 80 characters
 daily-motivation-quote --max-length 80
```

## Development & Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```

The tests are deterministic and use mocks, so they work offline.
