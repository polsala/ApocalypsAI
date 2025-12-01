# Nightly ISO8601 Duration Parser

Utility to parse ISO 8601 duration strings (e.g., `PT1H30M` or `P2W3DT4H5M6S`) into total seconds.

## Features
- Pure Python 3.11 implementation, no external dependencies.
- Callable function `parse_duration` for library use.
- Simple command‑line interface.

## Installation
Just copy the folder into your project or run the script directly; no installation step required.

## Usage
### As a library
```python
from src.parser import parse_duration

seconds = parse_duration("P2W3DT4H5M6S")
print(seconds)  # → 1471506
```

### As a CLI
```bash
python -m src.parser PT1H30M
# prints: 5400
```

## Supported components
- Weeks (`W`)
- Days (`D`)
- Hours (`H`)
- Minutes (`M`)
- Seconds (`S`)

The parser follows the subset of ISO 8601 defined in the implementation; months and years are intentionally omitted for deterministic conversion.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-iso8601-duration-parser/tests
```
