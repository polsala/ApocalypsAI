# nightly-rot13-encoder

A lightweight, zero‑dependency command‑line tool that applies the ROT13 cipher to a given string.

## Features
- Encode any UTF‑8 string with ROT13.
- Decode (ROT13 is symmetric, so the same operation works for both).
- Simple `--decode` flag for semantic clarity.
- Fully tested with deterministic offline unit tests.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and run the script directly with Python 3.11+
python -m utils.nightly-rot13-encoder.src.rot13 "Hello, World!"
# => Uryyb, Jbeyq!

python -m utils.nightly-rot13-encoder.src.rot13 --decode "Uryyb, Jbeyq!"
# => Hello, World!
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/nightly-rot13-encoder/tests
```
