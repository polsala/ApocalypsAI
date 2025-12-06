# Fortune Cookie Generator

A tiny, self‑contained utility that prints a random fortune cookie message to the console.  
You can optionally request a specific category (e.g., *wisdom*, *humor*, *tech*).

## Installation

The utility is pure Python 3.11 and has no external dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

*(Or just run the script directly – it lives in `src/fortune.py`.)*

## Usage

```bash
python -m src.fortune          # prints a random fortune
python -m src.fortune --category wisdom   # prints a wisdom‑type fortune
```

## How it works

The script stores a small hard‑coded list of fortunes, each tagged with one or more
categories. When invoked it picks a random entry (using `random.choice`) that matches
the requested category, if any.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```

The tests mock `random.choice` to guarantee deterministic output.
