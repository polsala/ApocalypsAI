# Random Compliment Generator

A whimsical utility that prints a random compliment to the console. Perfect for adding a bit of positivity to scripts, CI logs, or your daily terminal routine.

## Usage

```sh
python -m random_compliment_generator
```

Optional seed for reproducible output:

```sh
python -m random_compliment_generator --seed 42
```

## How it works

Selects a compliment from a built‑in list using `random.choice`. When a seed is supplied, `random.seed` ensures the same compliment is chosen each run.

## Tests

Run with:

```sh
python -m unittest discover -s utils/random-compliment-generator/tests
```
