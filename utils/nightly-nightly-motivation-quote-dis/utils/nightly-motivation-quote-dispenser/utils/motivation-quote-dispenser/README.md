# Nightly Motivation Quote Dispenser

A whimsical yet useful utility that prints a random motivational quote from a curated, offline collection. It can optionally filter quotes by tag (e.g., `inspiration`, `humor`). Perfect for adding a splash of positivity to CI runs, terminal sessions, or daily scripts.

## Installation

```bash
# From the repository root
python -m venv .venv
source .venv/bin/activate
pip install .
# Or simply run the script directly with the repository's Python interpreter.
```

## Usage

```bash
python -m utils.nightly-motivation-quote-dispenser.utils.motivation-quote-dispenser.src.quote_dispenser [--tag TAG]
```

- `--tag TAG` – Only consider quotes that contain the given tag. If omitted, any quote may be returned.

## Example

```bash
$ python -m utils.nightly-motivation-quote-dispenser.utils.motivation-quote-dispenser.src.quote_dispenser
“Believe you can and you're halfway there.” – Theodore Roosevelt
```

## Testing

```bash
pytest utils/nightly-motivation-quote-dispenser/utils/motivation-quote-dispenser/tests
```
