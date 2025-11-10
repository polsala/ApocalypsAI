# ASCII Art Clock

A tiny, self‑contained utility that prints the current time (or any `datetime`) as a three‑line ASCII‑art representation.

## Features
- No external dependencies – pure Python 3.11.
- Deterministic rendering; useful for scripts, demos, or just a bit of terminal whimsy.
- Includes a simple CLI (`python -m ascii_art_clock`) and a library function `render_time`.
- Fully tested with offline, deterministic unit tests.

## Usage
```bash
# As a module
python -m ascii_art_clock

# As a library
>>> from src.clock import render_time
>>> from datetime import datetime
>>> print(render_time(datetime(2023, 1, 1, 12, 34, 56)))
```

The output looks like:
```
    _   _      _  _ 
  | _|· _| |_|· |_ |_ 
  |_  _|  _|   ·  _| _|
```
*(The middle line uses a centered dot `·` for the colon.)*

## Implementation Details
- Digits are defined in a 3×3 bitmap stored in `DIGITS`.
- The colon is a special 3‑character pattern using `·`.
- `render_time(dt)` builds the three rows by concatenating the appropriate patterns with a single space separator.
- The module can be executed directly to print the current local time.

## Testing
Run the tests with:
```bash
python -m unittest discover -s utils/ascii-art-clock/tests
```
