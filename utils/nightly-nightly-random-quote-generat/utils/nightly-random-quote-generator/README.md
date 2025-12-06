# Random Quote Generator

`nightly-random-quote-generator` is a lightweight, self‑contained Python utility that prints a random quote each time it is executed.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic tests** – uses `unittest.mock` to control randomness.
- **CLI friendly** – run with `python -m random_quote_generator` or invoke the `quote` function from your own code.

## Installation

Copy the entire folder into your repository under `utils/nightly-random-quote-generator/` and add the path to your `PYTHONPATH` if needed.

```bash
# Example usage
python -m utils.nightly-random-quote-generator.utils.random-quote-generator.src.quote
```

## Usage

```python
from utils.nightly_random_quote_generator.utils.random_quote_generator.src.quote import get_random_quote

print(get_random_quote())
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-random-quote-generator/tests
```
