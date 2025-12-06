# Human Duration Parser

A tiny, zero‑dependency Python utility that converts human‑friendly duration strings into a total number of seconds.

## Features

- Supports weeks (`w`), days (`d`), hours (`h`), minutes (`m`), and seconds (`s`).
- Allows spaces or no spaces between components (e.g., `"1d4h"` or `"1d 4h"`).
- CLI wrapper (`python -m parser "2h30m"`) prints the result.
- Fully unit‑tested and offline.

## Installation

Copy the `utils/human-duration-parser` folder into your project or install it as a module:

```bash
pip install .  # from the repo root, after adding the folder to a package layout
```

Or simply run the script directly:

```bash
python -m utils.human-duration-parser.src.parser "3h 15m"
```

## Usage (Python)

```python
from utils.human-duration-parser.src.parser import parse_duration

seconds = parse_duration("2h30m")  # 9000
```

## Usage (CLI)

```bash
$ python -m utils.human-duration-parser.src.parser "1d 2h"
93600
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/human-duration-parser/tests
```
