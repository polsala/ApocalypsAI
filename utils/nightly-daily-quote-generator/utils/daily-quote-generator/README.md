# Daily Quote Generator

A tiny offline utility that returns a deterministic "daily" inspirational quote based on the current date. No network calls; all quotes are stored locally.

## Usage

```bash
python -m utils.daily-quote-generator.src.quote
```

Will print today's quote.

## How it works

The utility loads a static `quotes.json` list and selects an entry using the ordinal value of today's date modulo the number of quotes, ensuring the same quote is returned for a given date across runs and machines.
