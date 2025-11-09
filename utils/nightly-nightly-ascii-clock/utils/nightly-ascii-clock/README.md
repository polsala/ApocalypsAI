# Nightly ASCII Clock

A tiny utility that prints the current time as big ASCII‑art digits.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **Deterministic output** – easy to test by mocking `datetime`.
- **CLI friendly** – run with `python -m utils.nightly-ascii-clock.src.clock`.

## Usage

```bash
python -m utils.nightly-ascii-clock.src.clock
```

Will output something like:

```
 _   _       _   _   _   _   _   _ 
| | | |   |  _| |_  |_    | |_  |_|
|_| |_|   | |_   _|  _|   | |_   _|
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-ascii-clock/tests
```
