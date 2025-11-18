# Nightly Duration Parser

Utility to convert human‑readable duration strings into seconds.

## Supported units
- `d` – days
- `h` – hours
- `m` – minutes
- `s` – seconds

Units may appear in any order and can be separated by spaces, e.g. `2d 3h`, `1h30m`, `45s`.

## Installation
No external dependencies – just copy the folder and run the script with Python 3.11.

## Usage
```sh
python -m duration_parser "1h30m"
# => 5400
```

You can also import the library in your own code:
```python
from duration_parser import parse_duration
seconds = parse_duration("2d4h")
```

## Testing
```sh
cd utils/nightly-duration-parser
pytest -q
```
