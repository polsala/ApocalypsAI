# Galactic Time Converter

Convert between Unix timestamps and the whimsical **Galactic Standard Time (GT)** format.

GT is defined as `GT-YYYYMMDD-HHMMSS` and represents the Unix epoch shifted by **1,000,000 seconds** (≈11 days 13 h 46 m 40 s). This utility is completely offline and has no external dependencies.

## Usage

```bash
# Convert Unix → GT
python -m utils.galactic-time-converter.src.converter --to-gt 1609459200
# Output: GT-20210112-134640

# Convert GT → Unix
python -m utils.galactic-time-converter.src.converter --to-unix GT-20210112-134640
# Output: 1609459200
```

## API

- `unix_to_galactic(ts: int) -> str`
- `galactic_to_unix(gt: str) -> int`

Both raise `ValueError` on malformed input.

## Tests

Run the bundled tests with:

```bash
python -m unittest discover -s utils/galactic-time-converter/tests
```
