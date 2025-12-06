# Nightly Duration Parser

A tiny, self‑contained Python utility that converts human‑readable duration strings into total seconds and vice‑versa.

## Features
- Parse strings like `"2d 5h 30m"`, `"45m"`, `"1h30s"` into an integer number of seconds.
- Format an integer number of seconds back into a compact, readable string.
- No external dependencies – pure standard library.

## Usage
```python
from utils.nightly-duration-parser.src.parser import parse_duration, format_duration

seconds = parse_duration("2h 15m")   # → 8100
readable = format_duration(8100)      # → "2h 15m"
```

## Running the Tests
```bash
python -m unittest discover -s utils/nightly-duration-parser/tests
```

## License
MIT – see the root LICENSE file.
