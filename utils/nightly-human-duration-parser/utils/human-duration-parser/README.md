# Human Duration Parser

A tiny, zero‑dependency Python utility that converts human‑friendly duration strings into a total number of seconds.

## Features

- Supports weeks (`w`), days (`d`), hours (`h`), minutes (`m`), and seconds (`s`).
- Allows spaces or no spaces between components (e.g., `"1d4h"` or `"1d 4h"`).
- Provides a simple CLI: `python -m parser "2h30m"` → `9000`.
- Fully typed and includes a small test suite.

## Installation

Copy the `utils/human-duration-parser` folder into your project or install it as a module:

```bash
pip install .  # if you turn it into a package later
```

## Usage

```python
from parser import parse_duration

seconds = parse_duration("1d 2h 30m")
print(seconds)  # 93900
```

CLI:

```bash
python -m parser "45m"   # prints 2700
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
