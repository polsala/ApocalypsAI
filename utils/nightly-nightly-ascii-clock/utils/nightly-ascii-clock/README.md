# Nightly ASCII Clock

`nightly-ascii-clock` is a self‑contained utility that prints the current local time using big ASCII‑art digits.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic tests** – uses `unittest.mock` to freeze time.
- **CLI friendly** – run `python -m utils.nightly-ascii-clock.src.clock` to see the clock.

## Usage

```bash
# From the repository root
python -m utils.nightly-ascii-clock.src.clock
```

Output (example for 14:35):

```
  _   _       _   _ 
 | | | |   | | | | |
 |_| |_|   |_| |_| |
```

## Implementation Details

- The core logic lives in `src/clock.py`.
- Digits are represented by a 3‑row pattern dictionary.
- The CLI formats the current time (`%H:%M`) and prints the assembled ASCII art.

## Testing

Run the tests with:

```bash
python -m pytest utils/nightly-ascii-clock/tests
```

The test suite mocks `datetime.datetime.now` to ensure deterministic output.
