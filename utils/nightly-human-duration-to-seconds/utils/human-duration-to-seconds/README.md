# Human Duration to Seconds

Utility that converts human‑readable duration strings like `2h30m` or `1d 4h 5m 10s` into total seconds. Includes a tiny CLI.

## Installation

```bash
pip install .
```

(Assuming you add this folder to `PYTHONPATH` or install it as a package.)

## Usage

```bash
python -m utils.human-duration-to-seconds.src.duration_parser "2h30m"
# => 9000
```

Or import:

```python
from utils.human-duration-to-seconds.src.duration_parser import parse_duration
seconds = parse_duration("1d 2h")
```

## Supported units

- `d` – days
- `h` – hours
- `m` – minutes
- `s` – seconds

Units may appear in any order, optional whitespace, case‑insensitive.

## Tests

Run:

```bash
python -m unittest discover utils/human-duration-to-seconds/tests
```
