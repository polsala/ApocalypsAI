# Apocalypse Countdown Timer

A whimsical-yet-useful command-line utility to count down the time remaining until a specified future date and time, framed as an "apocalypse" event. Perfect for tracking project deadlines, release dates, or just a fun arbitrary future moment.

## Usage

Run the script with your target apocalypse date and time.

```bash
python src/countdown.py "YYYY-MM-DD HH:MM:SS"
```

### Examples

Count down to a specific date and time:
```bash
python src/countdown.py "2024-12-31 23:59:59"
```

If the target date is in the past, it will report how long ago it was:
```bash
python src/countdown.py "2020-01-01 00:00:00"
```

## Development

The utility is written in Python 3.11 and uses only standard library modules (`datetime`, `argparse`, `sys`).

## Tests

Tests are located in `tests/test_countdown.py` and use `unittest` with `unittest.mock` to ensure deterministic results by mocking the current time.
