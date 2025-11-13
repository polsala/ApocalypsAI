# ASCII Art Clock

A tiny, self‑contained Python utility that prints the current time using big ASCII digits. Perfect for adding a splash of retro charm to your terminal or scripts.

## Features
- No external dependencies – pure Python 3.11.
- Works offline; only uses the standard library.
- Provides a simple CLI (`python -m ascii_art_clock`) that prints the time.
- Includes a deterministic unit test suite that mocks the current time.

## Usage
```bash
# Run the clock directly
python -m ascii_art_clock
```

You can also import the helper function:
```python
from src.clock import render_time
from datetime import datetime

print(render_time(datetime.now()))
```

## Testing
```bash
python -m unittest discover -s utils/ascii-art-clock/tests
```
