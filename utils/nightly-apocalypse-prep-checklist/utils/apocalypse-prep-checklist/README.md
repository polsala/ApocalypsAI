# Apocalypse Prep Checklist Generator

This utility provides a fun yet surprisingly practical way to prepare for various end-of-the-world scenarios. Whether you're bracing for a zombie horde, an AI uprising, a meteor impact, or even an alien invasion, this tool will generate a tailored checklist to help you survive and thrive.

## Usage

To generate a checklist, run the `checklist_generator.py` script with the desired scenario name as an argument:

```bash
python src/checklist_generator.py <scenario_name>
```

**Available Scenarios:**
*   `zombie-outbreak`
*   `ai-uprising`
*   `meteor-impact`
*   `alien-invasion`

### Example:

```bash
python src/checklist_generator.py zombie-outbreak
```

This will print the 'Zombie Outbreak Survival Guide' checklist to your console.

## Development

The scenarios are defined in `src/scenarios.json`. You can add new scenarios or modify existing ones by editing this file. Each scenario requires a `title`, `description`, and a list of `items`.

## Testing

Tests are located in the `tests/` directory and can be run using `pytest`:

```bash
pytest tests/
```
