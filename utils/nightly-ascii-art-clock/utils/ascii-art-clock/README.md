# ASCII Art Clock

A whimsical yet useful utility that displays the current time in big ASCII‑art digits.

## Features
- Render any `datetime` object as a multi‑line ASCII representation.
- Command‑line interface (`python -m ascii_art_clock`) prints the current local time.
- Zero external dependencies – pure Python 3.11 standard library.

## Usage
```bash
# Run the clock (prints current time)
python -m utils.ascii-art-clock.src.clock
```

Or import the helper in your own code:
```python
from utils.ascii-art-clock.src.clock import render_time
from datetime import datetime

print(render_time(datetime.now()))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/ascii-art-clock/tests
```

The tests mock the current time to ensure deterministic output.
