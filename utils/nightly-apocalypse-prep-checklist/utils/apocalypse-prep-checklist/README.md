# Apocalypse Prep Checklist Generator

## Overview

This utility provides a fun, yet thought-provoking, way to prepare for various hypothetical apocalyptic scenarios. Whether you're bracing for a zombie outbreak, a meteor impact, or an AI uprising, this tool will generate a tailored checklist of essential preparations.

While the scenarios are whimsical, the underlying principles of preparedness (food, water, first aid, communication, skills) are genuinely useful for any emergency.

## Usage

To generate a checklist, run the `checklist_generator.py` script with your desired scenario. If no scenario is provided, a general preparedness checklist will be displayed.

### Available Scenarios:

*   `zombie`
*   `meteor`
*   `ai-uprising`
*   `solar-flare`
*   `general` (default)

### Examples:

```bash
# Get a general preparedness checklist
python src/checklist_generator.py

# Prepare for a zombie apocalypse
python src/checklist_generator.py --scenario zombie

# Prepare for an AI uprising
python src/checklist_generator.py --scenario ai-uprising
```

## Output Example (for `zombie` scenario):

```
--- Apocalypse Prep Checklist: Zombie Outbreak ---

1. Secure a safe house with multiple exits.
2. Stockpile non-perishable food and water (3-month supply).
3. Gather first-aid supplies and learn basic wound care.
4. Acquire sturdy blunt weapons (crowbar, baseball bat).
5. Practice silent movement and evasion tactics.
6. Identify reliable communication methods (walkie-talkies, ham radio).
7. Establish a rendezvous point with trusted allies.
```
