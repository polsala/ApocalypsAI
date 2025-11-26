# nightly-zen-quote-of-the-day

## Overview

`nightly-zen-quote-of-the-day` is a tiny, self‑contained Python utility that prints a **deterministic** Zen‑style quote for a given date (defaulting to today).  The quote is selected by taking the date's ordinal value and using it as an index into a static list of ten uplifting sayings.  No network access, no external data files – everything lives in the repository.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **Deterministic** – the same date always yields the same quote, making testing trivial.
- **CLI friendly** – run it directly or import the module.
- **Offline** – works without internet, perfect for CI or isolated environments.

## Installation

```bash
# From the repository root
cd utils/nightly-zen-quote-of-the-day
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for consistency)
```

## Usage

```bash
# Print today's quote
python -m src.quote

# Print a quote for a specific date (ISO format)
python -m src.quote --date 2022-12-25
```

## How it works

1. The utility defines a hard‑coded list of ten quotes.
2. For a given `datetime.date`, it computes `date.toordinal() % len(quotes)`.
3. The resulting index selects the quote, which is printed to stdout.

Because `date.toordinal()` is a stable integer, the mapping never changes.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```

The tests mock `datetime.date.today()` to guarantee repeatable results.
