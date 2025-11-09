# Nightly ASCII Clock

`nightly-ascii-clock` is a tiny, self‑contained utility that displays the current local time using big ASCII‑art digits.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **CLI friendly** – run `python -m src.clock` to print the time.
- **Deterministic tests** – the test suite mocks the system clock so it never depends on the real time.

## Usage

```bash
$ python -m src.clock
  _   _       _   _   _   _   _   _ 
 | | | |   |   | | | |   | | | | | |
 |_| |_|   |   |_| |_|   |_| |_| |_|
```

The output shows the hour and minute in `HH:MM` format (seconds are omitted for brevity).

## Running the tests

```bash
$ python -m unittest discover -s tests
```
