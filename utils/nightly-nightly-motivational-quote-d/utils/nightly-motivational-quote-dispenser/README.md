# Nightly Motivational Quote Dispenser

## Overview

`nightly-motivational-quote-dispenser` is a self‑contained utility that prints a random motivational quote to stdout. It ships with a curated list of uplifting sayings and works completely offline.

## Installation

The utility is pure Python 3.11 and has **no external dependencies**. Simply copy the `src/` directory into your Python path or run it directly:

```bash
python -m utils.nightly-motivational-quote-dispenser.src.quote_dispenser
```

## Usage

```bash
$ python -m utils.nightly-motivational-quote-dispenser.src.quote_dispenser
"The only way to do great work is to love what you do." – Steve Jobs
```

You can also import the module in your own scripts:

```python
from utils.nightly-motivational-quote-dispenser.src.quote_dispenser import get_random_quote
print(get_random_quote())
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-motivational-quote-dispenser/tests
```

All tests are deterministic and use mocks, so they work offline.
