# Daily Motivation Quote

`daily-motivation-quote` is a lightweight, zero‑dependency Python utility that prints a random motivational quote. It ships with a curated list of quotes, each optionally tagged with a category (e.g., *productivity*, *wellness*, *creativity*).

## Features

- **Random quote** – just run the tool and get a fresh line of encouragement.
- **Category filtering** – ask for a quote from a specific theme.
- **Deterministic mode** – supply a `--seed` to get reproducible output (useful for tests or scripts).
- **Pure Python 3.11** – no external packages, works offline.

## Installation

Copy the `utils/daily-motivation-quote` folder into your project and run the module directly:

```bash
python -m daily_motivation_quote
```

## Usage

```bash
# Random quote
python -m daily_motivation_quote

# Quote from a specific category
python -m daily_motivation_quote --category productivity

# Deterministic output (same quote every time with the same seed)
python -m daily_motivation_quote --seed 42
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-motivation-quote/tests
```
