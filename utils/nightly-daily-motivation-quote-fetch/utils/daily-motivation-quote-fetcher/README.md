# Daily Motivation Quote Fetcher

`daily-motivation-quote-fetcher` is a lightweight, self‑contained Python utility that prints a random motivational quote to standard output.

## Features
- No external network calls – quotes are bundled with the utility.
- Zero dependencies beyond the Python standard library.
- Simple CLI: `python -m src.quote_fetcher`.
- Deterministic unit tests using mocks.

## Usage
```bash
$ python -m src.quote_fetcher
"The only way to do great work is to love what you do." – Steve Jobs
```

## Installation
The utility is self‑contained; just copy the `utils/daily-motivation-quote-fetcher` folder into your project and run the module.

## Testing
```bash
$ python -m unittest discover -s tests
```
