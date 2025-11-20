# Nightly Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑inspired quote to the console. Optionally filter quotes by a tag (e.g., `mindfulness`, `humor`).

## Installation

```bash
pip install .
```

## Usage

```bash
python -m utils.nightly_zen_quote_generator.utils.zen_quote_generator.src.zen_quote [--tag TAG]
```

## Example

```
$ python -m utils.nightly_zen_quote_generator.utils.zen_quote_generator.src.zen_quote
“The obstacle is the path.” – Zen Proverb
```

## Testing

```bash
pytest utils/nightly-zen-quote-generator/utils/zen-quote-generator/tests
```
