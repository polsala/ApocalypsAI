# Nightly Relic Rarity Sorter

A type-safe CLI tool to classify and sort scavenged relics by perceived rarity and utility, aiding post-apocalyptic inventory management. Bring order to the chaos of your wasteland finds!

## Features

*   **Whimsical Classification**: Assigns rarity (Common, Uncommon, Rare, Legendary, Mythic) and a utility score (0-10) based on keywords.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **Customizable Rules**: Extend or override classification logic with your own JSON rule files.
*   **CLI Interface**: Easily classify items directly from your terminal.

## Installation

1.  Ensure you have Node.js (v16 or higher) and npm installed.
2.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-relic-rarity-sorter
    ```
3.  Install dependencies and build the project:
    ```bash
    npm install
    npm run build
    ```
4.  (Optional) Link the CLI tool globally for easy access:
    ```bash
    npm link
    ```
    Now you can run `relic-sorter` from any directory.

## Usage

Run the `relic-sorter` command followed by the names of your relics.

```bash
# Basic classification
relic-sorter "Rusty Spoon" "Gleaming Data-Chip" "Ancient Power-Cell"

# With descriptions
relic-sorter "Rusty Spoon" "Gleaming Data-Chip" -d "A very old and broken spoon." "An intact data storage unit."

# Using custom rules (example: create a custom-rules.json file)
# custom-rules.json:
# [
#   { "keywords": ["void-crystal"], "rarityBoost": "Mythic", "utilityBoost": 10, "description": "A powerful void-crystal." },
#   { "keywords": ["pet-rock"], "rarityBoost": "Common", "utilityBoost": 1, "description": "A loyal, but not very useful, pet rock." }
# ]
relic-sorter "Void-Crystal" "Pet Rock" --rules ./custom-rules.json
```

### Example Output

```
--- Classified Relics ---

Relic: Void-Crystal
  Rarity: \u001b[33mM\u001b[39m\u001b[33my\u001b[39m\u001b[33mt\u001b[39m\u001b[33mh\u001b[39m\u001b[33mi\u001b[39m\u001b[33mc\u001b[39m
  Utility Score: \u001b[36m10\u001b[39m/10
  Reasoning:
    - A powerful void-crystal.: void-crystal

Relic: Ancient Power-Cell
  Description: A pre-fall energy core, still pulsating faintly.
  Rarity: \u001b[34mR\u001b[39m\u001b[34ma\u001b[39m\u001b[34mre\u001b[39m
  Utility Score: \u001b[36m9\u001b[39m/10
  Reasoning:
    - Power sources are always valuable: power-cell
    - Historical significance, might hold secrets: ancient, pre-fall

Relic: Gleaming Data-Chip
  Description: An intact data storage unit.
  Rarity: \u001b[37mU\u001b[39m\u001b[37mn\u001b[39m\u001b[37mc\u001b[39m\u001b[37mo\u001b[39m\u001b[37mm\u001b[39m\u001b[37mm\u001b[39m\u001b[37mo\u001b[39m\u001b[37mn\u001b[39m
  Utility Score: \u001b[36m4\u001b[39m/10
  Reasoning:
    - Suggests good condition or aesthetic value: gleaming
    - Electronic components, potentially useful: data-chip

Relic: Rusty Spoon
  Description: A very old and broken spoon.
  Rarity: \u001b[90mC\u001b[39m\u001b[90mo\u001b[39m\u001b[90mm\u001b[39m\u001b[90mm\u001b[39m\u001b[90mo\u001b[39m\u001b[90mn\u001b[39m
  Utility Score: \u001b[36m0\u001b[39m/10
  Reasoning:
    - Indicates low quality or damage: broken, rusty

Relic: Pet Rock
  Rarity: \u001b[90mC\u001b[39m\u001b[90mo\u001b[39m\u001b[90mm\u001b[39m\u001b[90mm\u001b[39m\u001b[90mo\u001b[39m\u001b[90mn\u001b[39m
  Utility Score: \u001b[36m1\u001b[39m/10
  Reasoning:
    - A loyal, but not very useful, pet rock.: pet-rock
```

## Development

To run tests:
```bash
npm test
```

To run the development version directly:
```bash
npm run dev "Ancient Scroll" "Broken Robot Arm"
```
