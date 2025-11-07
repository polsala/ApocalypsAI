# Nightly ASCII Clock

A tiny, self‑contained utility that displays the current time in big ASCII‑art digits.

## Features

- **CLI**: `python -m nightly_ascii_clock` prints the current time in the terminal.
- **Library**: `nightly_ascii_clock.get_ascii_time(dt)` returns the ASCII representation for any `datetime` object.
- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic offline tests** using mocked datetime.

## Usage

```bash
# Run the CLI (prints the current local time)
python -m nightly_ascii_clock

# Use as a library
>>> from nightly_ascii_clock import get_ascii_time
>>> from datetime import datetime
>>> print(get_ascii_time(datetime(2025, 12, 31, 23, 59)))
 _   _   _   _   _   _   _   _   _   _ 
| | | | | | | | | | | | | | | | | | |
|_| |_| |_| |_| |_| |_| |_| |_| |_| |
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-ascii-clock/tests
```
