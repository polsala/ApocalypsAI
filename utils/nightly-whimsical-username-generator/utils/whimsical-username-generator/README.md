# Whimsical Username Generator

A tiny, self‑contained Python utility that creates playful usernames like `sparkly‑otter‑42`.

## Features

- **Deterministic** when a seed is supplied (perfect for tests).
- No external dependencies – only the Python standard library.
- Provides a small CLI (`python -m src.generator`) that prints a username to stdout.

## Usage

```bash
# Generate a random username
python -m utils/whimsical-username-generator/src/generator

# Generate a reproducible username (seed = 123)
python -m utils/whimsical-username-generator/src/generator --seed 123
```

## API

```python
from utils.whimsical-username-generator.src.generator import generate_username

# Random username
print(generate_username())

# Reproducible username
print(generate_username(seed=42))
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/whimsical-username-generator/tests
```
