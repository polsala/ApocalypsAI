# Daily Zen Quote Generator

`daily-zen-quote-generator` is a lightweight, zero‑dependency Python utility that prints a *quote of the day*.

## Features

- Deterministic selection based on the current date (same date → same quote).
- No external network calls – quotes are bundled in the package.
- Simple CLI: `python -m daily_zen_quote_generator`.
- Fully tested with offline mocks.

## Usage

```bash
python -m daily_zen_quote_generator
```

Will output something like:

```
“Be yourself; everyone else is already taken.” – Oscar Wilde
```

## Extending

Add more quotes to `src/quotes.json` following the existing JSON array format.

## License

MIT
