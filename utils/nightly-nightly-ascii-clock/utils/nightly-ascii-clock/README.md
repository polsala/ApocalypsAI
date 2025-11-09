# Nightly ASCII Clock

`nightly-ascii-clock` is a tiny, self‑contained Python utility that displays the current local time using big ASCII‑art digits. It’s perfect for adding a splash of retro charm to your terminal or for embedding in scripts that need a human‑readable timestamp.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic offline tests** – the test suite mocks the system clock, so it never requires network access.
- **Easy to use** – run the module directly with `python -m src.clock` or import the `get_ascii_time` function in your own code.

## Installation

Copy the entire `utils/nightly-ascii-clock/` folder into your project and run the script with Python 3.11 or later.

```bash
cd utils/nightly-ascii-clock
python -m src.clock
```

## API

```python
from src.clock import get_ascii_time

# Returns a multi‑line string containing the ASCII representation of the given datetime.
ascii_art = get_ascii_time(datetime.datetime.now())
```

## Testing

Run the bundled tests with the standard library `unittest` runner:

```bash
python -m unittest discover -s tests
```

The tests mock `datetime.datetime.now` to ensure deterministic output.
