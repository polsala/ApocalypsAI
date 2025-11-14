# Human Duration Parser

A tiny, self‑contained utility that converts human‑readable duration strings into total seconds.

## Features

- Supports days (`d`), hours (`h`), minutes (`m`), and seconds (`s`).
- Flexible ordering (e.g., `1h30m`, `30m1h`).
- Simple CLI for quick conversions.
- Fully typed, no external dependencies.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and run the CLI directly:
python -m utils.human-duration-parser.src.parser "2h45m"
```

The command prints the total number of seconds (`9900`).

## API

```python
from utils.human-duration-parser.src.parser import parse_duration

seconds = parse_duration("1d2h3m4s")  # => 93784
```

## Testing

```bash
python -m pytest utils/human-duration-parser/tests
```

All tests run offline and are deterministic.
