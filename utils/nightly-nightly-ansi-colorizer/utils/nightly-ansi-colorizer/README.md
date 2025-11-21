# nightly-ansi-colorizer

A whimsical yet practical utility that injects ANSI colour codes into plain‑text log messages. It highlights the words **error**, **warning**, and **info** with red, yellow, and green respectively, making terminal output easier to scan.

## Features
- Simple Python 3.11 implementation, no external dependencies.
- Works as a library (`colorize(text)`) or as a CLI (`python -m utils.nightly-ansi-colorizer.src.colorizer "Your message"`).
- Case‑insensitive keyword detection.

## Installation
Copy the `utils/nightly-ansi-colorizer` folder into your repository and run the tests to verify integrity:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (none needed)
python -m pytest utils/nightly-ansi-colorizer/tests
```

## Usage
### As a library
```python
from utils.nightly-ansi-colorizer.src.colorizer import colorize

msg = "Info: all systems go. Warning: low disk space. Error: failed to start."
print(colorize(msg))
```

### As a CLI
```bash
python -m utils.nightly-ansi-colorizer.src.colorizer "Info: all systems go."
```

The output will contain ANSI escape sequences that colour the keywords when printed to a compatible terminal.
