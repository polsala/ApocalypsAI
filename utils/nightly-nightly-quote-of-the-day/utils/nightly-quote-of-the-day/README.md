# Nightly Quote of the Day

`nightly-quote-of-the-day` is a self‑contained utility that prints a random inspirational quote from an internal list. No network access is required, making it safe to run in any environment (CI, local terminal, etc.).

## Usage

```sh
# Run directly via the module
python -m nightly_quote_of_the_day
```

or

```sh
python utils/nightly-quote-of-the-day/src/quote.py
```

The command prints a single quote to stdout.

## Design Goals

- **Zero external dependencies** – all quotes are bundled.
- **Deterministic tests** – the test suite mocks randomness.
- **Lightweight** – a single Python file, no additional packages.
