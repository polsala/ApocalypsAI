# Daily Motivation Quote

`daily-motivation-quote` is a lightweight, zero‑dependency Python utility that prints a random motivational quote each time it runs.

## Installation

```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/daily-motivation-quote
```

## Usage

```bash
python -m daily_motivation_quote
```

You can also import the function in your own code:

```python
from daily_motivation_quote import get_random_quote
print(get_random_quote())
```

## Testing

```bash
pytest utils/daily-motivation-quote/tests
```
