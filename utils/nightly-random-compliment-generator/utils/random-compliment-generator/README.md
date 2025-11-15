# Random Compliment Generator

A whimsical yet useful command‑line utility that prints a random compliment. It can be used in scripts, CI pipelines, or just for a quick morale boost.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **Deterministic mode** – supply a `--seed` to get reproducible output (useful for testing).
- **CLI friendly** – one‑liner: `python -m random_compliment_generator`

## Installation

Copy the `utils/random-compliment-generator` folder into your project and run:

```bash
python -m utils.random-compliment-generator.src.compliment
```

Or add the `src` directory to your `PYTHONPATH` and import the module.

## Usage

```bash
# Random compliment
python -m utils.random-compliment-generator.src.compliment

# Deterministic compliment (same seed → same output)
python -m utils.random-compliment-generator.src.compliment --seed 42
```

## API

```python
from utils.random-compliment-generator.src.compliment import get_compliment

# Get a random compliment
print(get_compliment())

# Get a reproducible compliment
print(get_compliment(seed=123))
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/random-compliment-generator/tests
```
