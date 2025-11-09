# Cat Fact Generator

A tiny, self‑contained utility that prints a random cat fact to standard output.

## Why?

Because every developer (and their CI pipelines) could use a quick dose of feline wisdom.

## Usage

```bash
python -m cat_fact_generator
```

Running the module will print one fact chosen at random from a curated list.

## Development

The implementation lives in `src/cat_fact_generator.py`.  Tests are provided under `tests/` and can be run with:

```bash
python -m unittest discover -s utils/cat-fact-generator/tests
```

The tests mock out randomness to stay deterministic and offline.
