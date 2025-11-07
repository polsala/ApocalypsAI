# Daily Zen Quote Generator

A lightweight, self‑contained Python utility that returns a random Zen‑inspired quote.  It can optionally filter quotes by a thematic category (e.g., *mindfulness*, *impermanence*, *simplicity*).  All quotes are stored locally – no network access required.

## Features

- **Zero external dependencies** – only the Python standard library.
- Choose a theme or let the utility pick from the full pool.
- Deterministic unit tests that mock the random selection.

## Installation

```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv
source .venv/bin/activate
pip install -e utils/daily-zen-quote-generator
```

## Usage

```python
from src.quote_generator import get_random_quote

# Any random quote
print(get_random_quote())

# Themed quote
print(get_random_quote(theme="mindfulness"))
```

## Running the tests

```bash
cd utils/daily-zen-quote-generator
python -m unittest discover -s tests
```

## Design notes

- Quotes are stored in a simple dictionary for easy extension.
- The helper `_flatten` builds a unified list when no theme is supplied.
- Tests replace `random.choice` with a mock to guarantee repeatable outcomes.
