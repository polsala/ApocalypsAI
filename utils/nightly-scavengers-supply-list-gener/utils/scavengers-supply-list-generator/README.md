# Scavenger's Supply List Generator

## Overview

In the desolate landscape of the post-apocalypse, resourcefulness is key to survival. The `Scavenger's Supply List Generator` is a whimsical-yet-useful command-line utility designed to aid survivors in their quest for essential items. Whether you're looking for a flashlight, a water filter, or a first-aid kit, this tool provides a breakdown of potential components, likely scavenging locations, and viable alternatives, helping you make the most of what's left.

## Features

*   **Item Breakdown**: Get a list of components required to assemble a specific item.
*   **Location Suggestions**: Discover common places where desired items or their components might be found.
*   **Alternative Solutions**: Learn about improvised or substitute items when the primary target is elusive.
*   **Extensible Data**: Easily add new items and their details to the `data.json` file.

## Installation

This utility is self-contained and written in Python 3.11. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/scavengers-supply-list-generator/` directory.
2.  The utility is ready to run.

## Usage

Run the `generator.py` script from the `src/` directory.

### Get a supply list for a specific item:

```bash
python src/generator.py flashlight
```

Example Output:

```
--- Scavenging Report for: Flashlight ---
Description: A portable light source.

Potential Components:
- Battery (2-4 (AA/AAA))
- Bulb (1 (LED preferred))
- Switch (1)
- Casing (1)

Likely Scavenging Locations:
- Abandoned homes
- Hardware stores
- Vehicles
- Tool sheds

Possible Alternatives:
- Candle
- Oil lamp
- Glow stick
- Solar lantern
```

### List all available items:

```bash
python src/generator.py --list
```

Example Output:

```
Available items for scavenging:
- First aid kit
- Flashlight
- Water filter
```

### Get help:

```bash
python src/generator.py --help
```

## Extending the Data

The utility's knowledge base is stored in `src/data.json`. You can easily add new items or modify existing ones by editing this file. The structure is straightforward:

```json
{
  "your new item": {
    "description": "A brief description of the item.",
    "components": [
      {"name": "component_name", "quantity": "e.g., 1, multiple, assorted"}
    ],
    "locations": ["location 1", "location 2"],
    "alternatives": ["alternative 1", "alternative 2"]
  }
}
```

Ensure the JSON remains valid after your edits.
