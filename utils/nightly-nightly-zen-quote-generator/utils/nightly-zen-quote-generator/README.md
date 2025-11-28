# Nightly Zen Quote Generator

Utility that prints a random Zen‑inspired quote to the console. Perfect for a brief pause of reflection amid chaos.

## Usage

```bash
# Run directly
python utils/nightly-zen-quote-generator/src/zen_quote.py

# Or as a module
python -m utils.nightly_zen_quote_generator.src.zen_quote
```

The command prints a single quote, e.g.:

```
When the mind is still, the universe surrenders.
```

## Implementation Details

- Quotes are stored in an internal list.
- `get_random_quote()` selects one using `random.choice`.
- The module can be executed as a script (`__main__`) to print the quote.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-zen-quote-generator/tests
```

The tests mock `random.choice` to guarantee deterministic output.
