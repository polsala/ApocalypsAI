# Apocalypse Prep Checklist

## Overview

The `apocalypse-prep-checklist` is a command-line utility designed to help you prepare for the inevitable (or just a really bad Tuesday). It generates a personalized survival checklist based on various whimsical apocalypse scenarios and the resources you already possess.

Whether you're bracing for a zombie horde, an EMP blast, or a full-blown AI uprising, this tool will give you a head start on your survival planning.

## Features

*   **Scenario-based Checklists**: Choose from a selection of pre-defined apocalypse scenarios.
*   **Resource Tracking**: Input your existing survival gear to see what you still need.
*   **Whimsical Advice**: Get a dose of humor and practical tips tailored to your chosen doom.
*   **Self-contained**: Runs entirely offline with no external dependencies beyond Python's standard library.

## How to Use

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/apocalypse-prep-checklist/src
    ```
2.  **Run the script**:
    ```bash
    python checklist_generator.py
    ```
3.  **Follow the prompts**: Select your desired apocalypse scenarios and list any survival items you already have.

## Example Output

```
Welcome, future survivor! Let's prepare for the end...

Select apocalypse scenarios (comma-separated, e.g., '1,3'):
1. Zombie Outbreak
2. Solar Flare / EMP
3. AI Uprising
Your choice: 1,2

Enter items you already have (comma-separated, e.g., 'Water filter,First aid kit'): water filter, flashlight

--- Your Personalized Apocalypse Prep Checklist ---

Scenario: Solar Flare / EMP
Description: The sun has unleashed its fury, frying electronics. Prepare for a world without power.

[ ] Battery-powered radio
[ ] Books and board games
[ ] Dust mask
[ ] Faraday cage (for sensitive electronics)
[HAVE] First aid kit
[HAVE] Flashlight and extra batteries
[ ] Hand-crank radio
[ ] Local maps
[ ] Manual can opener
[ ] Non-perishable food (3-day supply)
[ ] Solar charger (for small devices)
[ ] Water (1 gallon/person/day for 3 days)
[ ] Whistle
[ ] Wrench or pliers (to turn off utilities)

Whimsical Advice: Embrace the analog. Your smartphone is now a paperweight. Enjoy the stars!

Scenario: Zombie Outbreak
Description: The undead walk among us. Stay quiet, stay mobile, aim for the head.

[ ] Battery-powered radio
[ ] Crowbar or blunt weapon
[ ] Dust mask
[ ] Durable clothing (thick denim, leather)
[HAVE] First aid kit
[HAVE] Flashlight and extra batteries
[ ] Local maps
[ ] Manual can opener
[ ] Medical supplies for bites/scratches
[ ] Non-perishable food (3-day supply)
[ ] Quiet shoes
[ ] Water (1 gallon/person/day for 3 days)
[ ] Whistle
[ ] Wrench or pliers (to turn off utilities)

Whimsical Advice: Remember Rule #1: Cardio. And always double-tap.

--------------------------------------------------
Good luck, survivor! May your preps be plentiful and your doom be delayed.
```

## Development

This utility is written in Python 3.11 and uses only standard library modules. Tests are located in the `tests/` directory and can be run using `pytest` (or directly via `python -m unittest`).

## License

This utility is released under the [MIT License](../../../LICENSE).
