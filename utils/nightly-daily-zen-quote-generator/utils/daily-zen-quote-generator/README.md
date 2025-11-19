# Daily Zen Quote Generator

## Overview

`daily-zen-quote-generator` is a tiny, self‑contained Python utility that prints a random Zen‑style quote each time it is executed. It can be used as a light‑hearted way to inject positivity into command‑line tools, CI pipelines, or any Python script.

## Features

- **Zero external dependencies** – only the Python standard library.
- **Deterministic offline tests** – uses `unittest.mock` to guarantee repeatable results.
- **Simple CLI** – run `python -m src.zen_quote` to get a quote.

## Installation

Copy the `utils/daily-zen-quote-generator` folder into your repository and add it to your Python path, or install it as a package if you wish:

```bash
# From the repository root
python -m pip install -e utils/daily-zen-quote-generator
```

## Usage

```bash
python -m src.zen_quote
```

Or import the function in your own code:

```python
from src.zen_quote import get_random_quote
print(get_random_quote())
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
