# Apocalypse Prep Checklist Generator

A whimsical-yet-useful utility to generate a customizable survival checklist for various apocalyptic scenarios. Whether you're bracing for a zombie outbreak, a meteor impact, or an AI uprising, this tool helps you organize your preparations with a touch of dark humor.

## Features

*   **Scenario-Specific Checklists**: Get tailored recommendations for different types of apocalypses.
*   **General Survival Essentials**: Always includes a comprehensive list of basic survival items.
*   **Easy to Use**: Simple command-line interface.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Usage

Navigate to the `utils/apocalypse-prep-checklist` directory.

### Generate a general survival checklist:

```bash
python src/checklist_generator.py
# Or explicitly:
python src/checklist_generator.py general
```

### Generate a checklist for a specific scenario:

```bash
python src/checklist_generator.py zombie
python src/checklist_generator.py meteor
python src/checklist_generator.py ai-uprising
```

The output will be printed directly to your console.

## Available Scenarios

*   `general` (default)
*   `zombie`
*   `meteor`
*   `ai-uprising`

If an unknown scenario is provided, the utility will default to the `general` survival checklist.

## Development

### Running Tests

To ensure everything is working as expected, run the tests from the `utils/apocalypse-prep-checklist` directory:

```bash
python -m unittest tests/test_checklist_generator.py
```

## Contributing

Feel free to add more apocalyptic scenarios or essential survival items!
