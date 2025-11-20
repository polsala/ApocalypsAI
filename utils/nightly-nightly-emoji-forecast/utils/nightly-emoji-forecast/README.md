# Nightly Emoji Forecast

Utility that provides a whimsical weather forecast expressed in emojis for any given date. The forecast is deterministic: the same date always yields the same emoji sequence, making it safe for offline use and testing.

## Features

- CLI: `python -m emoji_forecast [--date YYYY-MM-DD]`
- Programmatic API: `get_forecast(date: datetime.date) -> str`
- No external dependencies beyond the Python standard library.

## Usage

```bash
$ python -m emoji_forecast
🌤️  Partly sunny

$ python -m emoji_forecast --date 2023-10-31
🎃  Spooky vibes (just for fun!)
```

(Example output may vary.)

## Implementation Details

The forecast selects an emoji from a curated list based on a seeded random generator derived from the date's ordinal value, ensuring reproducibility.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
