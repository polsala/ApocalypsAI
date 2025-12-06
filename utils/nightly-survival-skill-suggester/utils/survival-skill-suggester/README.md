# ApocalypsAI Survival Skill Suggester

## Overview

In the unpredictable world of ApocalypsAI, preparedness is key! The `survival-skill-suggester` is a lightweight, standalone Python utility designed to offer whimsical-yet-useful survival skill suggestions based on a keyword you provide. Whether you're bracing for a zombie outbreak, an AI uprising, or just a bad Tuesday, this tool will point you towards a crucial skill to master.

## Features

*   **Keyword-driven suggestions**: Get a relevant survival skill and a brief, engaging description.
*   **Core survival categories**: Covers essentials like water, food, shelter, first aid, defense, navigation, and fire.
*   **Self-contained**: No external dependencies beyond standard Python libraries.
*   **CLI-friendly**: Easy to run directly from your terminal.

## Usage

To get a skill suggestion, simply run the script with your chosen keyword:

```bash
python src/suggester.py <keyword>
```

### Examples

*   **For water-related skills:**
    ```bash
    python src/suggester.py water
    ```
    _Output: Skill: Water Purification, Description: Learn to filter and boil water..._

*   **For food-related skills (case-insensitive):**
    ```bash
    python src/suggester.py FOOD
    ```
    _Output: Skill: Foraging & Edible Plant Identification, Description: Distinguish between nourishing greens..._

*   **Using a secondary keyword:**
    ```bash
    python src/suggester.py hydration
    ```
    _Output: Skill: Water Purification, Description: Learn to filter and boil water..._

*   **If no skill is found:**
    ```bash
    python src/suggester.py aliens
    ```
    _Output: No specific skill found for 'aliens'. Try 'water', 'food', 'shelter', 'first aid', 'defense', 'navigation', or 'fire'._

## Development

This utility is written in Python 3.11 and is designed to be easily extensible. You can add more skills or categories by modifying the `SKILLS_DATABASE` dictionary in `src/suggester.py`.

## Tests

To run the automated tests for this utility, navigate to the `utils/survival-skill-suggester/` directory and execute:

```bash
python -m unittest tests/test_suggester.py
```
