# Human Duration Parser

Parse human‑readable duration strings like `2h30m`, `45s`, `1d 2h`, etc., into total seconds. The utility is pure Python, has no external dependencies, and includes a tiny command‑line interface.

## Features

- Supports days (`d`), hours (`h`), minutes (`m`), and seconds (`s`).
- Units can be combined in any order, with optional whitespace.
- Case‑insensitive.
- Provides a `parse_duration` function for programmatic use.
- Stand‑alone CLI: `python -m utils.human-duration-parser.src.parser "1d 2h30m"`

## Installation

Copy the `utils/human-duration-parser` folder into your project or clone the repository. No additional packages are required.

## Usage

```bash
# CLI example
python -m utils.human-duration-parser.src.parser "1d 2h30m"
# => 93900
```

```python
# Programmatic example
from utils.human-duration-parser.src.parser import parse_duration
seconds = parse_duration('45m15s')
print(seconds)  # 2715
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/human-duration-parser/tests
```

All tests are deterministic and run offline.
