# Daily Zen Quote Generator

Provides a simple command‑line tool that prints a random Zen‑inspired quote. Useful for a quick mental break.

## Installation

Copy the folder into your repository and run the module with Python 3.11:

```bash
python -m utils.daily-zen-quote-generator.src.zen
```

You can also add the `src` directory to your `PYTHONPATH` and invoke `zen` directly.

## Usage

```bash
# Print a completely random quote
python -m utils.daily-zen-quote-generator.src.zen

# Print a random quote from a specific theme
python -m utils.daily-zen-quote-generator.src.zen --theme nature
```

## Themes

- **nature**
- **mindfulness**
- **perseverance**

## Testing

The utility ships with deterministic unit tests that run offline. From the utility root:

```bash
pytest
```
