# human-delta

**human-delta** is a whimsical‑yet‑useful command‑line tool that takes two ISO‑8601 timestamps and prints the elapsed time in a friendly, English description (days, hours, minutes, seconds).

## Features
- Pure‑Python, no third‑party dependencies.
- Works as a library (`human_delta.diff`) **and** as a CLI (`python -m human_delta ...`).
- Handles timezone‑aware `datetime` objects.
- Deterministic unit tests with no network access.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/human-delta
```

## Usage
```bash
# Library
>>> from human_delta import diff
>>> diff("2023-01-01T12:00:00", "2023-01-03T15:30:45")
'2 days, 3 hours, 30 minutes, 45 seconds'

# CLI
python -m human_delta 2023-01-01T12:00:00 2023-01-03T15:30:45
# → 2 days, 3 hours, 30 minutes, 45 seconds
```

## Testing
```bash
pytest utils/human-delta/tests
```
