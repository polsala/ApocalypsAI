# ISO8601 Duration Parser

Utility to parse ISO 8601 duration strings (e.g., `PT1H30M`) into a total number of seconds.

## Usage
```python
from src.parser import parse_iso8601_duration

seconds = parse_iso8601_duration("PT2H45M10S")
print(seconds)  # 9910
```

Supported components:
- Days (`P3D`)
- Hours (`PT4H`)
- Minutes (`PT5M`)
- Seconds (`PT6S`)

The parser follows the subset of ISO 8601 used by most APIs and is deterministic, requiring no external resources.
