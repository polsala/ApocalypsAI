# Apocalypse Prep Checklist Generator

Prepare for the inevitable with the `apocalypse-prep-checklist` utility! This tool helps you generate a customized survival checklist based on various doomsday scenarios, ensuring you're ready for anything from a zombie outbreak to an AI uprising.

## Features

*   **Scenario-based Checklists**: Get tailored recommendations for specific apocalypse types.
*   **Base Essentials**: Always includes fundamental survival items.
*   **Customizable**: Add your own unique items to the list.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required.

```bash
cd utils/apocalypse-prep-checklist
```

## Usage

Run the script directly from its directory:

```bash
python src/checklist_generator.py --scenario zombie
```

### Arguments:

*   `--scenario <type>`: Specify the apocalypse scenario. Supported types: `zombie`, `ai_uprising`, `solar_flare`, `economic_collapse`. (Required)
*   `--no-base`: Exclude the general base survival items from the checklist. (Optional)
*   `--custom <item1> <item2> ...`: Add one or more custom items to your checklist. (Optional)

### Examples:

**1. Generate a checklist for a zombie apocalypse:**

```bash
python src/checklist_generator.py --scenario zombie
```

**2. Prepare for an AI uprising, excluding base items and adding custom gear:**

```bash
python src/checklist_generator.py --scenario ai_uprising --no-base --custom "EMP device" "Offline knowledge database"
```

**3. Get a general economic collapse checklist with extra cash:**

```bash
python src/checklist_generator.py --scenario economic_collapse --custom "Physical gold/silver" "Extra canned goods"
```
