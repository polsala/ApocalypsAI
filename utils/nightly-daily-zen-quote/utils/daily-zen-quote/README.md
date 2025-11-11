# Daily Zen Quote

`daily-zen-quote` is a tiny, zero‑dependency Python utility that prints a random Zen‑style quote each time it is run. It can be used in shell prompts, CI logs, or anywhere you need a quick dose of calm.

## Installation

```bash
# Copy the folder somewhere in your PATH
cp -r utils/daily-zen-quote ~/my-tools/
export PATH="$PATH:~/my-tools/daily-zen-quote/src"
```

## Usage

```bash
$ daily-zen-quote
"The obstacle is the path."
```

## How it works

The script selects a quote from a hard‑coded list using Python's `random.choice`. No network access is required, making it safe for offline environments.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote/tests
```
