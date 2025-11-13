# Daily Motivation Quote Fetcher

A whimsical yet useful command‑line utility that prints a random motivational quote to inspire your day. No external network calls; quotes are bundled within the script.

## Usage

```bash
python -m daily_motivation_quote_fetcher
# or
python src/main.py
```

## How it works

The script contains a small list of quotes and selects one at random using Python's `random.choice`. It can also be imported and used programmatically via `get_random_quote()`.

## Testing

Run the tests with:

```bash
pytest -q
```
