# Nightly Emoji Forecast

`nightly-emoji-forecast` is a tiny, self‑contained Python utility that prints a deterministic "weather" forecast represented by an emoji for a given date. The forecast is purely deterministic – it depends only on the calendar date – so it can be used in scripts, CI messages, or just for a daily smile.

## Features
- No external dependencies beyond the Python standard library.
- Deterministic output: the same date always yields the same emoji.
- Simple CLI (`python -m forecast [YYYY-MM-DD]`).
- Fully unit‑tested with offline mocks.

## Usage
```bash
# Install (no installation needed – just run the module)
python -m utils/nightly-emoji-forecast/src/forecast          # uses today
python -m utils/nightly-emoji-forecast/src/forecast 2025-04-01  # specific date
```

## How it works
The utility maps the ordinal value of the date (`date.toordinal()`) to an index in a short list of weather‑related emojis. Because `toordinal()` is monotonic, the mapping is repeatable and evenly distributed.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```
