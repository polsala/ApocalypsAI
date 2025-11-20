# Nightly Survival Skill Scribe

A handy Python utility for the discerning survivor, the Nightly Survival Skill Scribe allows you to store, retrieve, and search vital knowledge snippets for those moments when quick recall is paramount. Whether it's "how to purify water" or "basic first aid for radiation burns," keep your essential wisdom organized and accessible.

## Features

*   **Add/Update Skills**: Easily store new survival tips or refine existing ones.
*   **Retrieve Skills**: Look up specific skills by name.
*   **List All Skills**: Get an overview of all your accumulated wisdom.
*   **Search by Keyword**: Find relevant skills even if you only remember a fragment of their name or description.
*   **Persistent Storage**: Your knowledge is saved to a local JSON file, ready for the next blackout.

## Installation

This utility is self-contained. No special installation steps are required beyond having Python 3.11+ installed.

## Usage

The `scribe.py` script can be run directly from the command line.

```bash
# Add a new skill
python src/scribe.py add "Water Purification" "Boil water for 1 minute, or use iodine tablets. Filter through cloth first."

# Update an existing skill
python src/scribe.py update "Water Purification" "Boil water for 3 minutes at rolling boil, or use 2 drops of bleach per liter. Filter through cloth first."

# Get a skill by name
python src/scribe.py get "Water Purification"

# List all skills
python src/scribe.py list

# Search for skills containing "first aid"
python src/scribe.py search "first aid"

# Search for skills containing "purify" (case-insensitive)
python src/scribe.py search "purify"
```

## Data Storage

Skills are stored in a JSON file named `skills.json` within the `src/` directory. This file is automatically created and managed by the `scribe.py` script.

## Development & Testing

To run the tests, navigate to the `utils/nightly-survival-skill-scribe/` directory and execute:

```bash
python -m unittest tests/test_scribe.py
```
