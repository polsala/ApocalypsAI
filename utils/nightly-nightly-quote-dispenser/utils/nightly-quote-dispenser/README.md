# Nightly Quote Dispenser

`nightly-quote-dispenser` is a self‑contained, zero‑dependency Python utility that prints a random motivational quote each time it runs.

## Features
- **Offline** – quotes are baked into the source; no network calls.
- **Deterministic tests** – uses `unittest.mock` to control randomness.
- **Lightweight** – single file, no external packages.

## Installation
```bash
# From the repository root
cd utils/nightly-quote-dispenser
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m src.quote_dispenser
```

You’ll see a random quote printed to stdout.

## Testing
```bash
python -m unittest discover -s tests
```

All tests run offline and are fully deterministic.
