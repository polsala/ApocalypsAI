# Nightly Survival Tip Generator

A tiny utility that prints a random post‑apocalyptic survival tip. Great for adding a bit of levity to daily stand‑ups or CI logs.

## Usage

```sh
python -m tip_generator
```

Will output a tip like:

> "Always keep a spare bottle of water in your boot."

## How it works

The package ships with a static list of 20 tongue‑in‑cheek tips. `get_random_tip()` picks one using `random.choice`. The CLI simply prints the result.

## Testing

Run `pytest` in the `tests/` directory.
