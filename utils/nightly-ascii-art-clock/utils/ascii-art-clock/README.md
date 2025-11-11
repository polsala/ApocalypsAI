# ASCII Art Clock

A whimsical yet useful utility that displays the current time in a retro ASCII‑art style.

## Features
- Prints the current local time as large, readable ASCII digits.
- Deterministic output when a specific `datetime` is supplied (useful for testing).
- Zero external dependencies – pure Python 3.11.

## Usage
```bash
python -m utils.ascii-art-clock.src.clock
```

You can also import the helper function:
```python
from utils.ascii-art-clock.src.clock import ascii_time

print(ascii_time(datetime.datetime.now()))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/ascii-art-clock/tests
```

The tests mock the current time to ensure deterministic output.
