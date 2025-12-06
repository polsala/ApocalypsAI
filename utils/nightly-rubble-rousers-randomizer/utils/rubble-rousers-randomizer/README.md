# Rubble-Rouser's Randomizer

## Whimsical Utility for the ApocalypsAI Community

### Overview

The `Rubble-Rouser's Randomizer` is a simple, command-line utility designed to spark creativity for anyone navigating or crafting stories in a post-apocalyptic world. Whether you're a tabletop RPG Game Master needing a quick encounter, a writer looking for plot inspiration, or just curious about what you might find after the end, this tool provides random, thematic 'finds' and 'encounters'.

It's lightweight, self-contained, and requires no external dependencies beyond standard Python libraries.

### Usage

To use the randomizer, navigate to its directory and run the `randomizer.py` script. You can specify a category or let it pick one for you.

```bash
# Generate a random item from any category
python src/randomizer.py

# Generate a random 'Scavenged Item'
python src/randomizer.py --category item

# Generate a random 'Encounter'
python src/randomizer.py --category encounter

# Generate a random 'Location Detail'
python src/randomizer.py --category location
```

### Examples

```
$ python src/randomizer.py
Category: Item
Find: A working flashlight, but no spare batteries

$ python src/randomizer.py --category encounter
Category: Encounter
Find: A pack of feral dogs, eyeing your supplies

$ python src/randomizer.py --category location
Category: Location Detail
Find: A bridge partially destroyed, but still passable on foot
```

### Categories

*   `item`: Random objects or resources found.
*   `encounter`: Interactions with other survivors, creatures, or events.
*   `location`: Descriptive details about the environment.
