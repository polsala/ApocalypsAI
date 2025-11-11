# Fortune Cookie Generator

A tiny utility that prints a random fortune cookie message to stdout. It can be used directly from the command line or imported as a Python module.

## Features
- Returns a random, uplifting message from a curated list.
- Zero external dependencies – pure Python 3.11.
- Includes a deterministic test suite using mocks.

## Installation
Simply copy the `utils/fortune-cookie-generator` folder into your project or run it directly from this repository.

## Usage
```bash
python -m fortune_cookie_generator
```
Or, from Python code:
```python
from fortune_cookie_generator import get_fortune
print(get_fortune())
```

## Running the Tests
```bash
python -m unittest discover -s utils/fortune-cookie-generator/tests
```

## License
MIT © ApocalypsAI
