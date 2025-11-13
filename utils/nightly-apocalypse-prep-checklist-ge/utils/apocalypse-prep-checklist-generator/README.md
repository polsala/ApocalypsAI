# Apocalypse Prep Checklist Generator

Prepare for the inevitable with the `apocalypse-prep-checklist-generator`! This whimsical yet surprisingly practical command-line utility helps you get ready for various end-of-days scenarios. Whether it's a zombie horde, an AI uprising, or a devastating solar flare, this tool will provide you with a personalized checklist to ensure your survival (and perhaps a few laughs).

## Usage

To generate a checklist, simply run the script with your desired scenario:

```bash
python src/checklist_generator.py --scenario "zombie-outbreak"
```

To see a list of available scenarios:

```bash
python src/checklist_generator.py --list-scenarios
```

### Available Scenarios:

*   `zombie-outbreak`
*   `ai-uprising`
*   `solar-flare`
*   `alien-invasion`
*   `robot-rebellion`

## Installation

This utility is self-contained and requires Python 3.11+.

1.  Navigate to the `utils/apocalypse-prep-checklist-generator/` directory.
2.  Run the script directly:
    ```bash
    python src/checklist_generator.py --scenario "ai-uprising"
    ```

## Development

To add new scenarios or modify existing ones, edit `src/checklist_generator.py`.

## Tests

Run tests using `pytest` (install with `pip install pytest`):

```bash
pytest tests/test_checklist_generator.py
```
