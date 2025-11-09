# Random Compliment Generator

A whimsical command‑line utility that prints a random compliment. Choose a category (e.g., *creative*, *technical*, *general*) or let it surprise you.

## Installation

```bash
pip install .
# or just run the script directly:
python -m utils.random-compliment-generator.src.compliment
```

## Usage

```bash
# Random compliment
python -m utils.random-compliment-generator.src.compliment

# Specific category
python -m utils.random-compliment-generator.src.compliment --category creative
```

## How it works

The utility ships a small hard‑coded list of compliments grouped by category. It selects one with `random.choice`. No network access required.

## Testing

```bash
python -m unittest discover utils/random-compliment-generator/tests
```
