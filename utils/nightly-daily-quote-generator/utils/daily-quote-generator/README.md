# Daily Quote Generator

A tiny, self‑contained utility that serves up uplifting (or humorous) quotes.

## Features

- **Random quote** – deterministic when a seed is supplied.
- **Category filter** – limit results to `inspiration`, `humor`, or `wisdom`.
- **Quote of the day** – a reproducible “daily” quote based on the current date (mockable in tests).
- **Zero external dependencies** – everything lives in the repository.

## Usage

```bash
python -m src.quote_generator            # random quote
python -m src.quote_generator --seed 42   # deterministic random quote
python -m src.quote_generator --category humor   # random humor quote
python -m src.quote_generator --today    # quote of the day
```

## Running the tests

```bash
python -m unittest discover -s tests
```
