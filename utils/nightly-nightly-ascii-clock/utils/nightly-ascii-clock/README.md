# Nightly ASCII Clock

`nightly-ascii-clock` prints the current local time in large, block‑style ASCII art.  It can be used in terminal dashboards, CI logs, or any place you want a quick visual cue of the time.

## Usage

```bash
# Run as a module (Python 3.11+ required)
python -m utils.nightly-ascii-clock.src.clock
```

Or import the helper function in your own code:

```python
from utils.nightly-ascii-clock.src.clock import get_ascii_time
import datetime

now = datetime.datetime.now()
print(get_ascii_time(now))
```

## How it works

Each decimal digit (0‑9) is mapped to a 5‑line, 5‑character wide block representation.  `get_ascii_time` builds the four‑digit string `HHMM` (24‑hour clock) and stitches the corresponding blocks together with two spaces between digits.

## Testing

Run the bundled tests with:

```bash
pytest utils/nightly-ascii-clock/tests
```

The tests are deterministic and use no external network calls.
