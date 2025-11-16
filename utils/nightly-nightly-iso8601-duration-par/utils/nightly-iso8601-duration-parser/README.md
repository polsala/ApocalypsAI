# nightly‑iso8601‑duration‑parser

A tiny, self‑contained utility that parses ISO‑8601 duration strings into a dictionary of time components.

## Features

- Pure Python 3.11 – no external dependencies.
- Supports years, months, weeks, days, hours, minutes, and seconds.
- Command‑line interface for quick ad‑hoc parsing.
- Fully unit‑tested with deterministic offline tests.

## Usage

```bash
# As a module
python -m utils.nightly-iso8601-duration-parser.src.duration_parser "P1Y2M3DT4H5M6S"

# As a library
from utils.nightly-iso8601-duration-parser.src.duration_parser import parse_iso8601_duration
print(parse_iso8601_duration("PT20M"))
```

## Expected Output

```json
{"years": 1, "months": 2, "weeks": 0, "days": 3, "hours": 4, "minutes": 5, "seconds": 6}
```

## Testing

Run the tests with:

```bash
python -m unittest discover -s utils/nightly-iso8601-duration-parser/tests
```
