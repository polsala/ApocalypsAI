# Random Compliment Generator

A whimsical yet useful utility that prints a random compliment to the console. You can optionally filter compliments by category (e.g., *creative*, *technical*, *general*).

## Features
- Zero‑dependency Python 3.11 script.
- Deterministic unit tests using mocks.
- Simple CLI: `python -m random_compliment_generator [--category <cat>]`.

## Installation
```bash
# Clone the repository (or copy this folder) and install the utility locally
cd utils/random-compliment-generator
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage
```bash
# Print any random compliment
python -m random_compliment_generator

# Print a random compliment from the "creative" category
python -m random_compliment_generator --category creative
```

## Development
Run the test suite with:
```bash
pytest -q
```
