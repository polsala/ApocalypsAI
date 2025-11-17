# Nightly Emoji Forecast

A whimsical utility that gives you an emoji "forecast" for any given date. Useful for adding fun mood indicators to logs, commit messages, or daily stand‑ups.

## Usage

```bash
python -m forecast <YYYY-MM-DD>
# Example:
python -m forecast 2025-12-25
# Output: 🎄
```

The utility is **deterministic**: the same date always yields the same emoji.

## How it works

- Parses the input date.
- Computes a SHA‑256 hash of the ISO date string.
- Maps the hash to one of 20 emojis representing moods, weather, or events.

## Testing

Run `pytest` in the utility folder:

```bash
cd utils/nightly-emoji-forecast
pytest
```
