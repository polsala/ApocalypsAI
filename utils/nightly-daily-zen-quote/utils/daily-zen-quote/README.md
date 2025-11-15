# Daily Zen Quote

`daily-zen-quote` is a lightweight command‑line utility that prints a random Zen‑inspired quote.

## Features

- **Random quote** from a curated list of five timeless sayings.
- **Deterministic mode** – provide `--seed <int>` to get the same quote every time (useful for testing or reproducible scripts).
- Zero external dependencies; works with the standard library only.

## Installation

Copy the `src/quote.py` file into your project or add the whole folder to your `PATH`.

```bash
chmod +x utils/daily-zen-quote/src/quote.py
ln -s $(pwd)/utils/daily-zen-quote/src/quote.py /usr/local/bin/daily-zen-quote
```

## Usage

```bash
# Random quote
$ daily-zen-quote
The obstacle is the path.

# Deterministic quote (seed = 1)
$ daily-zen-quote --seed 1
The journey of a thousand miles begins with one step.
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote/tests
```
