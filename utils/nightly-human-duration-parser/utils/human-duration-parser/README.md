# Human Duration Parser

A tiny, self‑contained utility that converts human‑readable duration strings into a total number of seconds.

## Features

- Supports days (`d`), hours (`h`), minutes (`m`), and seconds (`s`).
- Order‑agnostic (e.g., `1h30m` and `30m1h` are both valid).
- Ignores whitespace and is case‑insensitive.
- Provides a simple command‑line interface.

## Installation

The utility is pure Python 3.11 and has **no external dependencies**. Simply copy the `utils/human-duration-parser/` folder into your project or add it as a submodule.

## Usage

```bash
python -m utils.human-duration-parser.src.parser "2h 30m"
# → 9000
```

Or import the function in your own code:

```python
from utils.human-duration-parser.src.parser import parse_duration

seconds = parse_duration("1d4h")  # 122400
```

## Supported format

The parser accepts a string consisting of one or more integer‑unit pairs:

- `d` – days
- `h` – hours
- `m` – minutes
- `s` – seconds

Examples:

- `"45s"` → 45
- `"3m15s"` → 195
- `"2h"` → 7200
- `"1d2h30m"` → 93900

Whitespace between components is ignored, and the units are case‑insensitive.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/human-duration-parser/tests
```

All tests are deterministic and run offline.
