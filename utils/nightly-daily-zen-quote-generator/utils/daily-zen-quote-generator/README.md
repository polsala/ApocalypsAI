# Daily Zen Quote Generator

Utility that returns a *Zen* quote of the day based on the current date. It works completely offline – the quotes are bundled in a small JSON file.

## Usage

```bash
# Run as a module (Python 3.11+ required)
python -m daily_zen_quote_generator
```

or directly execute the script:

```bash
python utils/daily-zen-quote-generator/src/main.py
```

The program prints a single line containing the quote.

## How it works

1. A static `quotes.json` file lives next to the source code.
2. The current date (`datetime.date.today()`) is converted to an ordinal number.
3. The ordinal is modulo‑ed by the number of quotes to pick a deterministic entry.
4. The selected quote is printed.

Because the algorithm is pure and deterministic, the same date always yields the same quote.

## Testing

The test suite mocks `datetime.date.today()` to guarantee deterministic output without any network calls.
