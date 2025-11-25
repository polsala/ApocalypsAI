# Daily Motivation Quote Fetcher

Utility that prints a random motivational quote to stdout. Useful for terminal startup scripts, Git hooks, or just a daily smile.

## Installation

```bash
pip install .
```

*(Assumes you add the package to a virtual environment or install it locally.)*

## Usage

```bash
python -m daily_motivation_quote_fetcher
```

or

```bash
python -c "from src.quote_fetcher import main; main()"
```

## How it works

Quotes are stored in a hard‑coded list. The `get_random_quote` function picks one using `random.choice`. The CLI prints it.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-motivation-quote-fetcher/tests
```
