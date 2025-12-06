# Random Compliment Generator

A lightweight, zero‑dependency Python utility that prints a random compliment to stdout.

## Features
- **Whimsical**: Brighten your day (or a teammate’s) with a friendly line.
- **Deterministic tests**: Uses `unittest.mock` to stub randomness.
- **Self‑contained**: No external APIs, works completely offline.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/random-compliment-generator
```

## Usage
```bash
python -m utils.random-compliment-generator.src.compliment
```

You’ll see a random compliment printed, e.g.:
```
Your curiosity is a superpower.
```

## Development & Testing
```bash
cd utils/random-compliment-generator
pytest
```

The test suite mocks the random selection to guarantee deterministic output.
