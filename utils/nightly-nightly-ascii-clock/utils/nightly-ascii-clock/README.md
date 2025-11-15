# Nightly ASCII Clock

## Overview

`nightly-ascii-clock` prints the current local time in a big, readable ASCII‑art style. It works entirely offline, has no external dependencies beyond the Python standard library, and includes a deterministic test suite that mocks the system clock.

## Features

- **Instant visual time** – large digits make the time easy to spot.
- **Zero‑dependency** – pure Python 3.11, no third‑party packages.
- **CLI friendly** – run `python -m src.clock` from the utility folder.
- **Tested** – deterministic unit tests using `unittest.mock`.

## Usage

```bash
cd utils/nightly-ascii-clock
python -m src.clock   # prints the current time as ASCII art
```

You can also import the helper function:

```python
from src.clock import get_ascii_time
print(get_ascii_time(datetime.datetime.now()))
```

## Development

Run the test suite with:

```bash
pytest -q
```

The tests mock the current time, so they are fully deterministic and require no network access.
