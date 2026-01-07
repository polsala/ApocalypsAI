# Nightly Cosmic Choice Weaver

## Summary
The `nightly-cosmic-choice-weaver` is a whimsical-yet-useful command-line interface (CLI) tool designed to help you make decisions when faced with a multitude of options. It takes a list of predefined choices, applies configurable "cosmic influences" (like weighted tags), and then, with a "stellar alignment," suggests the most appropriate path forward. It's perfect for when decision fatigue sets in, or you just want a little cosmic nudge.

## Features
- **Type-Safe Configuration**: Define your choices and influences using clear, type-checked interfaces.
- **Weighted Decision Making**: Assign base weights to choices and apply multipliers based on tags to influence the selection process.
- **Deterministic Results**: Use a `--seed` argument to ensure the same input always yields the same cosmic suggestion, useful for testing or consistent guidance.
- **Whimsical Output**: Presents suggestions with a touch of cosmic flair.
- **Self-Contained**: All dependencies and logic are bundled for easy use.

## Installation
1.  Navigate to the `typescript-utils/nightly-cosmic-choice-weaver` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```

## Usage
Run the tool using `ts-node` or by building it first.

### Using the default example choices:
```bash
npm start
# or
yarn start
```

### Using a custom configuration file:
Create a `config.json` file (see example below) and pass its path:
```bash
npm start -- --config ./path/to/your/config.json
# or
yarn start -- --config ./path/to/your/config.json
```

### Using a specific seed for deterministic results:
```bash
npm start -- --seed "my-lucky-star"
# or
yarn start -- --seed "my-lucky-star"
```

### Combined options:
```bash
npm start -- --config ./path/to/your/config.json --seed "solar-flare-event"
# or
yarn start -- --config ./path/to/your/config.json --seed "solar-flare-event"
```

### Help message:
```bash
npm start -- --help
# or
yarn start -- -h
```

## Configuration File (`config.json` example)
```json
{
  "choices": [
    {
      "id": "explore-wastes",
      "name": "Explore the Whispering Wastes",
      "description": "Seek out new resources and dangers.",
      "tags": ["adventure", "risky"],
      "weight": 10
    },
    {
      "id": "refactor-detector",
      "name": "Refactor the Temporal Anomaly Detector",
      "description": "Improve the core systems for future stability.",
      "tags": ["productive", "safe"],
      "weight": 15
    },
    {
      "id": "brew-infusion",
      "name": "Brew a Calming Herbal Infusion",
      "description": "Relax and recharge after a long cycle.",
      "tags": ["relaxing", "safe"],
      "weight": 8
    },
    {
      "id": "organize-cache",
      "name": "Organize the Survival Cache",
      "description": "Ensure all supplies are accounted for and secure.",
      "tags": ["productive", "safe"],
      "weight": 12
    },
    {
      "id": "decipher-whispers",
      "name": "Decipher Ancient Void Whispers",
      "description": "Uncover forgotten knowledge, or madness.",
      "tags": ["mystery", "risky"],
      "weight": 7
    }
  ],
  "influences": [
    { "tag": "risky", "multiplier": 0.7 },      // Disfavor risky choices slightly
    { "tag": "productive", "multiplier": 1.5 }, // Favor productive choices
    { "tag": "relaxing", "multiplier": 1.2 }    // Slightly favor relaxing choices
  ]
}
```

### Choice Object Properties:
- `id` (string, required): A unique identifier for the choice.
- `name` (string, required): The display name of the choice.
- `description` (string, optional): A longer explanation of the choice.
- `tags` (string[], optional): An array of tags associated with the choice (e.g., "adventure", "productive").
- `weight` (number, optional): A base numerical weight for this choice. Defaults to 1 if not provided. Higher weights make the choice more likely.

### CosmicInfluence Object Properties:
- `tag` (string, required): The tag this influence applies to.
- `multiplier` (number, required): A multiplier applied to the `weight` of any choice possessing this tag. A value > 1 increases likelihood, < 1 decreases it.

## Development
### Build the project:
```bash
npm run build
```

### Run tests:
```bash
npm test
```
