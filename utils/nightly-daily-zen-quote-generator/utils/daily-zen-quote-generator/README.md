# Daily Zen Quote Generator

Utility that returns a deterministic "quote of the day" based on the current date. It ships with an embedded list of Zen‑inspired quotes and selects one by hashing the date, ensuring the same quote is returned for a given day without any network calls.

## Usage

```bash
python -m src.quote_generator
```

Outputs a single line quote.

## How it works

- A static list of quotes lives in the source file.
- The current date (YYYY‑MM‑DD) is hashed with SHA‑256.
- The hash is turned into an integer and modulo‑ed by the number of quotes.
- The selected quote is printed.

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```
