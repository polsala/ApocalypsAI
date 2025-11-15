# Daily Quote Fetcher

`daily-quote-fetcher` is a tiny, self‑contained Python utility that prints a random inspirational quote to the console.  It can optionally filter quotes by a simple category (e.g., *inspiration*, *life*, *philosophy*).

## Features
- No external dependencies – pure Python 3.11.
- Offline – quotes are baked into the source.
- Deterministic unit tests using mocks.

## Installation
```bash
# From the repository root
cd utils/daily-quote-fetcher
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for consistency)
```

## Usage
```bash
python -m src.quote_fetcher            # any random quote
python -m src.quote_fetcher --category inspiration   # only inspiration quotes
```

## Testing
```bash
python -m unittest discover -s tests
```
