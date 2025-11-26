# Silly Username Generator

A tiny, self‑contained utility that creates whimsical usernames.

## Features

- Combines a random adjective, noun, and a 2‑digit number.
- Deterministic when a seed is supplied (useful for testing).
- Simple CLI for quick generation.

## Usage

```bash
python -m utils.silly-username-generator.src.generator --count 5 --seed 123
```

Will output something like:
```
fluffy-unicorn42
spooky-robot07
...```

## API

```python
from utils.silly-username-generator.src.generator import generate_username

# Default generation
name = generate_username()

# Custom word lists
name = generate_username(
    adjectives=["brave", "cunning"],
    nouns=["dragon", "wizard"],
    seed=99
)
```

## Testing

Run the bundled tests with:
```bash
python -m unittest discover utils/nightly-silly-username-generator/utils/silly-username-generator/tests
```
