# Random Compliment Generator

A tiny utility that prints a random compliment to the console. Great for adding a bit of positivity to scripts, CI logs, or just your day.

## Installation

```bash
pip install .
# or copy the src folder into your project
```

## Usage

```bash
python -m random_compliment_generator
```

or

```bash
python -c "from random_compliment_generator import get_compliment; print(get_compliment())"
```

## How it works

The script selects a compliment from a hard‑coded list using `random.choice`. The list is curated to be friendly and inclusive.

## Testing

Run the tests with:

```bash
python -m unittest discover -s utils/random-compliment-generator/tests
```
