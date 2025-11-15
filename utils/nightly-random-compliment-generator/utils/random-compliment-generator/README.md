# Random Compliment Generator

A lightweight, self‑contained utility that prints a random compliment to the console.  It can optionally limit compliments to a specific category (e.g., *work*, *creative*, or *general*).

## Features
- Zero external dependencies beyond the Python standard library.
- Deterministic, offline unit tests using `unittest.mock`.
- Simple CLI (`python -m src.compliment`) with `--category` flag.

## Installation
```bash
# Clone the repository (or copy this folder) and navigate into it
cd utils/random-compliment-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (no requirements needed for this utility)
```

## Usage
```bash
# Print any random compliment
python -m src.compliment

# Print a random compliment from the "work" category
python -m src.compliment --category work
```

## Testing
```bash
python -m unittest discover -s tests
```

The tests are deterministic and do not require network access.
