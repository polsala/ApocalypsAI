# Nightly Survival Skill Scribe

## Overview

The `nightly-survival-skill-scribe` is a whimsical yet practical command-line utility designed to equip you with essential knowledge for navigating the unexpected. Whether you're facing a zombie apocalypse, a power outage, or just a bad day, this scribe will dispense a random, actionable survival tip to keep your wits sharp and your spirit resilient.

It's like having a grizzled old survivalist whispering wisdom directly into your terminal, but without the questionable hygiene.

## Features

*   **Random Tip Dispenser**: Get a new, surprising tip every time you run it.
*   **Category Filtering**: Focus on specific areas like 'Shelter', 'Water', 'First Aid', or 'Morale'.
*   **List Categories**: See all available categories to explore.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-survival-skill-scribe/` directory.
2.  (Optional but recommended) Create and activate a Python virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

## Usage

To get a random survival tip:

```bash
python3 src/scribe.py
```

To get a tip from a specific category (e.g., 'Water'):

```bash
python3 src/scribe.py --category Water
```

To list all available categories:

```bash
python3 src/scribe.py --list-categories
```

## Example Output

```
>>> python3 src/scribe.py

--- Survival Tip --- 
Category: First Aid
Tip: Always carry a basic first-aid kit. Know how to use it for minor cuts, burns, and sprains.
--------------------

>>> python3 src/scribe.py --category Shelter

--- Survival Tip --- 
Category: Shelter
Tip: If caught in the open, seek natural shelters like caves or dense foliage. Prioritize protection from elements.
--------------------

>>> python3 src/scribe.py --list-categories

Available Categories:
- Communication
- Fire
- First Aid
- Food
- Morale
- Navigation
- Observation
- Preparedness
- Self-Defense
- Shelter
- Tools
- Water
--------------------
```

## Contributing

Feel free to add more survival tips or categories by modifying `src/scribe.py` and submitting a pull request!
