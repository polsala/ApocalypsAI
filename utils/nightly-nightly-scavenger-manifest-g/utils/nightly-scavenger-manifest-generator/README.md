# Nightly Scavenger Manifest Generator

## Overview
In the desolate landscape of the post-apocalypse, keeping track of your precious finds is paramount. The `nightly-scavenger-manifest-generator` is a simple, yet indispensable, utility designed to help you catalog your scavenged items. It takes a plain text file listing your discoveries and transforms it into a neatly organized Markdown manifest, grouped by category, making your inventory easily readable and searchable.

## Features
- **Categorized Output**: Organizes items under clear category headings.
- **Tagging Support**: Includes item-specific tags for more detailed descriptions.
- **Markdown Format**: Generates a human-readable Markdown file, compatible with most text editors and viewers.
- **Timestamped Manifests**: Each manifest includes the generation date for historical tracking.

## Usage

### Input File Format
Create a text file (e.g., `scavenged_items.txt`) where each line represents an item. The format for each line should be:

`Item Name | Category | Tag1, Tag2, Tag3`

- **Item Name**: The primary name of the item (e.g., "Rusty wrench").
- **Category**: The main classification for the item (e.g., "Tools", "Food").
- **Tags**: An optional, comma-separated list of descriptive tags (e.g., "repair", "melee", "long-shelf-life").

**Example `scavenged_items.txt`:**
```
Rusty wrench | Tools | repair, melee
Can of beans | Food | edible, long-shelf-life, protein
Tattered map | Info | navigation, paper
Broken radio | Electronics | salvage, broken
Medical kit (partial) | Medical | first-aid, bandages
```

### Running the Generator

```bash
python src/manifest_generator.py --input scavenged_items.txt --output my_manifest.md
```

- `--input` (or `-i`): Path to your input text file containing scavenged items.
- `--output` (or `-o`): Path where the generated Markdown manifest will be saved.

### Example Output (`my_manifest.md`)

```markdown
# Scavenger's Manifest - 2023-10-27

## Electronics
- Broken radio (salvage, broken)

## Food
- Can of beans (edible, long-shelf-life, protein)

## Info
- Tattered map (navigation, paper)

## Medical
- Medical kit (partial) (first-aid, bandages)

## Tools
- Rusty wrench (repair, melee)
```

## Development

The utility is written in Python 3.11 and has no external dependencies beyond the standard library. Tests are located in the `tests/` directory.
