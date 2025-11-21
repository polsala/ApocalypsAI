# nightly-iso8601-duration-parser

A tiny, self‑contained Python utility that converts ISO 8601 duration strings into a total number of seconds.

## Features

- Supports the most common subset of ISO 8601 durations (`PnDTnHnMnS`).
- No external dependencies – pure Python 3.11 standard library.
- Includes a simple CLI for quick ad‑hoc conversions.
- Fully tested with deterministic unit tests.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-iso8601-duration-parser
```

```bash
# CLI usage
python -m nightly_iso8601_duration_parser.src.parser PT1H30M
# → 5400
```

Or use it as a library:

```python
from nightly_iso8601_duration_parser.src.parser import parse_iso8601_duration
seconds = parse_iso8601_duration("P2DT3H")  # 2 days + 3 hours = 183600 seconds
```

## Testing

```bash
pytest utils/nightly-iso8601-duration-parser/tests
```

All tests run offline and are deterministic.
