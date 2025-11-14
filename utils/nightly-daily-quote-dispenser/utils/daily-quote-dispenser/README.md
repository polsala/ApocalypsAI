# Daily Quote Dispenser

`daily-quote-dispenser` is a lightweight, zero‑dependency Python utility that prints a random inspirational quote each time you run it. Great for adding a splash of positivity to your terminal or scripts.

## Features
- **Built‑in quote library** – no network calls required.
- **Deterministic tests** – uses mocks to guarantee repeatable results.
- **Simple CLI** – just run the script, or import the function in your own code.

## Installation
```bash
# Clone the repository (or copy the folder) and install the utility in a virtual environment.
python -m venv .venv
source .venv/bin/activate
pip install -e utils/daily-quote-dispenser
```

## Usage
```bash
python -m daily-quote-dispenser
```
Or, from Python:
```python
from daily_quote_dispenser.src.quote import get_random_quote
print(get_random_quote())
```

## Testing
```bash
pytest utils/daily-quote-dispenser/tests
```
All tests run offline and are fully deterministic.
