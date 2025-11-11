# Daily Quote Generator

Utility that prints a random inspirational quote to the console. Great for adding a splash of motivation to your terminal, shell startup scripts, or CI logs.

## Features
- No external dependencies – everything is bundled.
- Deterministic unit tests using mocks.
- Simple CLI (`python -m utils.daily-quote-generator.src.quote`).

## Installation
```bash
# No extra packages required; just copy the folder or install the repo in editable mode.
python -m pip install -e .
```

## Usage
```bash
python -m utils.daily-quote-generator.src.quote
```

You will see a randomly selected quote, e.g.:
```
"The only limit to our realization of tomorrow is our doubts of today."
    — Franklin D. Roosevelt
```

## Testing
```bash
pytest utils/daily-quote-generator/tests
```
