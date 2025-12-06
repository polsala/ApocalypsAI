# ASCII Art Clock

A whimsical yet useful utility that displays the current local time in a retro 7‑segment ASCII‑art style.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **CLI entry point** – run `python -m ascii_art_clock` to print the time.
- **Deterministic tests** – offline unit tests mock `datetime.datetime.now`.

## Usage

```bash
$ python -m ascii_art_clock
  _   _       _   _   _   _   _   _ 
 | | | |   |  _| |_  |_    | |_  |_|
 |_| |_|   | |_   _|  _|   | |_   _|
```

The output shows `HH:MM` in large ASCII digits.

## Implementation Details

- `src/clock.py` contains the core rendering logic.
- `tests/test_clock.py` validates the rendering for known timestamps and ensures the CLI uses the mocked time.
