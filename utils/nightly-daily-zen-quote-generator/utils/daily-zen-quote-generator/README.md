# Daily Zen Quote Generator

Utility that prints a zen‑like quote of the day. No network required; it uses a built‑in list of quotes and selects one deterministically based on the current date.

## Usage
```bash
python -m src.main
```
Running the command prints a single quote to stdout.

## How it works
The script computes the number of days since the Unix epoch (1970‑01‑01) and uses that value modulo the number of available quotes to pick one. This makes the output repeatable for any given date and completely offline.

## Testing
The utility ships with a small `unittest` suite that mocks the current date to verify deterministic behaviour. Run the tests with:
```bash
python -m unittest discover -s tests
```
