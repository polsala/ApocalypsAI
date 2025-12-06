# Nightly Survival Skill Tracker

## Overview

Welcome, intrepid survivor! The `nightly-survival-skill-tracker` is a whimsical command-line utility designed to help you assess and improve your readiness for any unforeseen global events. Whether you're honing your foraging techniques or perfecting your first-aid skills, this tool provides a simple way to track your progress and identify areas for improvement.

## Features

*   **Add Skills**: Easily add new survival skills to your personal tracker.
*   **Rate Skills**: Assign a rating (1-5) to each skill, reflecting your proficiency.
*   **List Skills**: View all your tracked skills and their current ratings.
*   **Suggest Improvement**: Get a recommendation for which skill to focus on next, typically the one with the lowest rating (alphabetically chosen if multiple have the same lowest rating).

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-survival-skill-tracker/` directory.
2.  You can run the script directly:
    ```bash
    python3 src/tracker.py --help
    ```

## Usage

The `tracker.py` script uses `argparse` for its command-line interface.

### Add a new skill

```bash
python3 src/tracker.py add "Foraging for Edible Plants"
```

### Rate an existing skill

Ratings are from 1 (beginner) to 5 (master).

```bash
python3 src/tracker.py rate "First Aid" 4
```

### List all skills

```bash
python3 src/tracker.py list
```

### Get a suggestion for improvement

```bash
python3 src/tracker.py suggest
```

## Data Storage

Your skills data is stored in a simple JSON file named `skills.json` within the `src/` directory. This keeps the utility self-contained and easy to manage.

## Contributing

Feel free to fork, modify, and improve this tracker! Suggestions for new features or bug fixes are always welcome.
