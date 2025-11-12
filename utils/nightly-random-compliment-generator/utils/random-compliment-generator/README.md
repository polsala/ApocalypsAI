# Random Compliment Generator

A whimsical yet useful utility that prints a random compliment to the console. You can optionally specify a category (e.g., `work`, `friendship`, `creativity`) to get a themed compliment.

## Features
- Zero‑dependency Python 3.11 script.
- Deterministic behavior in tests via mocking.
- Extensible list of compliments and categories.

## Installation
Simply copy the `utils/random-compliment-generator` folder into your repository and run the script with Python:

```bash
python -m utils.random-compliment-generator.src.compliment [--category CATEGORY]
```

## Usage
```bash
# Any random compliment
python -m utils.random-compliment-generator.src.compliment

# A compliment about work
python -m utils.random-compliment-generator.src.compliment --category work
```

## Development & Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/random-compliment-generator/tests
```

The tests mock the random selection to ensure deterministic outcomes.
