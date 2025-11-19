# Nightly Zen Quote Generator

## Overview

`nightly-zen-quote-generator` is a self‑contained Python utility that prints a single, deterministic "Zen" quote each day. The quote is chosen from a curated list based on the current date, so the output is repeatable and requires no network access.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic** – the same date always yields the same quote.
- **CLI friendly** – run `python -m src.zen` to get today’s quote.
- **Tested** – includes offline unit tests with mocked dates.

## Usage

```bash
python -m src.zen          # prints today’s quote
python -m src.zen 2025-12-01  # prints the quote for a specific ISO date
```

## Adding New Quotes

Edit the `QUOTES` list in `src/zen.py`. Each entry should be a short, inspirational sentence.
