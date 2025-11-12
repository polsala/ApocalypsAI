# Random Compliment Generator

A whimsical yet useful utility that prints a random compliment to stdout.

## Features
- Choose from several compliment categories (e.g., *general*, *code*, *life*).
- Fully self‑contained Python 3.11 implementation – no external dependencies.
- Deterministic, offline unit tests using `unittest.mock`.

## Installation
```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Navigate to the utility folder
cd utils/random-compliment-generator

# (Optional) Create a virtual environment
python -m venv .venv && source .venv/bin/activate
```

## Usage
```bash
python -m src.compliment            # prints a random compliment
python -m src.compliment --category code   # prints a random "code" compliment
```

## Running the Tests
```bash
python -m unittest discover -s tests
```

## License
MIT © ApocalypsAI
