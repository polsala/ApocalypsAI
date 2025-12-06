# Daily Motivation Notifier

A tiny CLI utility that prints a random motivational quote to stdout. Perfect for adding a splash of positivity to your terminal sessions.

## Installation

```bash
pip install .
# or just run the script directly:
python -m utils.daily-motivation-notifier.src.main
```

## Usage

```bash
python -m utils.daily-motivation-notifier.src.main
# or
python utils/daily-motivation-notifier/src/main.py
```

## How it works

The script contains a hard‑coded list of uplifting quotes. When executed it selects one at random using Python's `random.choice` and prints it.

## Testing

```bash
pytest utils/daily-motivation-notifier/tests
```
