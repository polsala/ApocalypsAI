# Human Duration Parser

A tiny, zero‑dependency utility that converts human‑readable duration strings into a total number of seconds.

## Features

- Supports days (`d`), hours (`h`), minutes (`m`), and seconds (`s`).
- Order‑agnostic (e.g., `5h2d` works the same as `2d5h`).
- Simple Python API: `parse_duration("1d2h30m") -> 93900`.
- Small command‑line interface `duration-to-seconds`.

## Installation

Just copy the folder `utils/human-duration-parser/` into your project and import:

```python
from utils.human-duration-parser.src.parser import parse_duration
```

## Usage

### Library

```python
from utils.human-duration-parser.src.parser import parse_duration

seconds = parse_duration("1d 2h 30m")
print(seconds)  # 93900
```

### CLI

```bash
$ python -m utils.human-duration-parser.src.parser "3h45m"
13500
```

## Supported format

- Numbers must be integers (no floats).
- Units: `d` (days), `h` (hours), `m` (minutes), `s` (seconds).
- Whitespace is ignored.
- Example valid strings: `"2d"`, `"5h30m"`, `"45m10s"`, `"1d 2h 3m 4s"`.

## Error handling

Invalid strings raise a `ValueError` with a helpful message.
