# Nightly Mutant Morale Booster

## Overview

In the grim darkness of the post-apocalyptic future, there is still... a little bit of dark humor and survival wisdom! The Nightly Mutant Morale Booster is a simple command-line utility designed to deliver a daily dose of uplifting (or comically grim) messages, affirmations, and survival tips to keep the community's spirits from completely crumbling. Because even mutants need a pick-me-up.

## Features

*   **Daily Wisdom**: Generates a unique message each day based on the current date.
*   **Whimsical & Useful**: Combines dark humor with genuinely useful (or at least thought-provoking) survival insights.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Usage

To get your daily morale boost, simply run the script:

```bash
python src/booster.py
```

The script will print a message to your console.

## Example Output

```
>>> python src/booster.py
[Morale Booster] Remember, every day without a zombie bite is a good day!
```

```
>>> python src/booster.py
[Morale Booster] Today's forecast: 90% chance of survival, 10% chance of finding a working toaster. Stay vigilant!
```

## Development

### Running Tests

To ensure the morale booster is always in top shape, run the tests:

```bash
python -m unittest tests/test_booster.py
```
