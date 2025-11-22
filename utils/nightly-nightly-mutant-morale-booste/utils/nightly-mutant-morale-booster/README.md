# Nightly Mutant Morale Booster

## Overview

In the grim darkness of the post-apocalyptic future, a little cheer goes a long way. The Nightly Mutant Morale Booster is a simple utility designed to inject a daily dose of whimsical inspiration or a quirky survival tip directly into your terminal. Whether you're fending off irradiated squirrels or just trying to find a working toaster, this booster ensures your spirits remain... somewhat intact.

## Features

*   **Randomized Wisdom**: Delivers a new, hand-picked quote or tip with each run.
*   **Apocalyptic Charm**: All messages are flavored with the unique despair and resilience of the wasteland.
*   **Lightweight & Self-Contained**: No external dependencies, just pure Pythonic morale.

## Usage

To get your daily dose of mutant morale, simply run the `booster.py` script:

```bash
python src/booster.py
```

The script will print a random morale-boosting message to your console.

## Examples

```
>>> python src/booster.py
[MUTANT MORALE BOOSTER] Remember: Even a broken clock is right twice a day. Just like your Geiger counter.
```

```
>>> python src/booster.py
[MUTANT MORALE BOOSTER] Survival Tip: Always check for extra limbs before sharing your last can of beans.
```

## Development

The core logic resides in `src/booster.py`. New quotes and tips can be added to the `MORALE_MESSAGES` list within that file.

## Testing

Tests are located in `tests/test_booster.py`. To run them:

```bash
python -m unittest tests/test_booster.py
```
