# Daily Zen Quote Generator

Utility that returns a deterministic Zen quote for a given date. The same date always yields the same quote, making it perfect for:

- Daily stand‑up intros
- Commit message inspiration
- Terminal MOTD scripts

## Usage

```bash
# Install (no external dependencies required)
# Run with an explicit date (YYYY‑MM‑DD)
python -m utils.daily-zen-quote-generator.src.main 2023-10-31

# Or let it use today’s date
python -m utils.daily-zen-quote-generator.src.main
```

## How it works

The utility contains a small curated list of Zen‑style sayings. It selects a quote by converting the supplied date to an integer (`YYYYMMDD`) and taking the modulo with the number of quotes. This guarantees deterministic output without any network calls.
