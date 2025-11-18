# UUID Shortener

Utility to convert a standard UUID (36‑character hyphenated string) into a shorter Base‑62 representation (typically 22 characters) and back again.

## Features
- **Encode** a UUID to a compact Base‑62 string.
- **Decode** a Base‑62 string back to the canonical UUID format.
- Simple command‑line interface.
- Pure Python 3.11, no external dependencies.

## Installation
The utility is self‑contained. Clone the repository and run the module directly:

```bash
python -m shortener encode <uuid>
python -m shortener decode <short>
```

Or import the functions in your own code:

```python
from shortener import encode_uuid, decode_uuid

short = encode_uuid("123e4567-e89b-12d3-a456-426614174000")
original = decode_uuid(short)
```

## Why Base‑62?
Base‑62 uses the characters `0‑9A‑Za‑z`, making the output URL‑safe without needing additional encoding.

## License
MIT – see the repository LICENSE file.
