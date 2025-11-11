# Daily Motivational Quote

`daily-motivational-quote` is a lightweight, zero‑dependency Python utility that prints a random motivational quote each time it is run.  You can also filter quotes by a simple *category* (e.g., `work`, `life`, `confidence`).

## Installation

The utility is self‑contained – just copy the `src/` directory into your project or add the whole folder to your `PYTHONPATH`.

```bash
# From the repository root
cp -r utils/daily-motivational-quote ~/my-tools/
```

## Usage

```bash
python -m daily-motivational-quote.src.quote          # any quote
python -m daily-motivational-quote.src.quote -c work   # only "work" quotes
```

You can also import the helper function in your own code:

```python
from daily_motivational_quote.src.quote import get_random_quote

print(get_random_quote())
```

## Development & Testing

Run the bundled tests with the standard library `unittest` runner:

```bash
python -m unittest discover -s utils/daily-motivational-quote/tests
```

All tests are deterministic and use mocks; no network access is required.
