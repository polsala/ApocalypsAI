# Daily Zen Quote

Prints a random Zen‑inspired quote to the console. Optionally filter by theme.

## Installation

Copy the folder into your project and run:

```bash
python -m utils.daily-zen-quote.src
```

or

```bash
python -m utils.daily-zen-quote.src.__main__ --theme nature
```

## Usage

- `python -m utils.daily-zen-quote.src` prints a random quote.
- `python -m utils.daily-zen-quote.src --theme <theme>` prints a random quote from that theme.

Available themes: `nature`, `mindfulness`, `humor`.

## Testing

Run tests with:

```bash
python -m unittest discover utils/daily-zen-quote/tests
```
