# Random Compliment Generator

A whimsical utility that prints a random compliment to brighten your day. It can also produce deterministic compliments when given a seed, making it useful for scripts or testing.

## Installation

```bash
# No external dependencies required beyond the Python standard library.
```

## Usage

```bash
python -m utils.random-compliment-generator.src.main
# or
python utils/random-compliment-generator/src/main.py
```

You can also specify a seed for reproducible output:

```bash
python -c "from utils.random-compliment-generator.src.main import get_compliment; print(get_compliment(seed=42))"
```

## License

MIT
