# Apocalypse Prep Checklist Generator

A whimsical-yet-useful utility to generate a personalized apocalypse preparedness checklist based on various scenarios and locations. Whether you're bracing for a zombie horde, a nuclear winter, or an AI uprising, this tool has you covered with both practical and delightfully specific advice.

## Features

*   **Scenario-Specific Items**: Get tailored recommendations for different apocalypse types (e.g., `zombie`, `nuclear`, `ai_uprising`, `alien_invasion`, `climate_collapse`).
*   **Location-Specific Items**: Adapt your prep for your environment (e.g., `urban`, `rural`, `coastal`, `mountain`).
*   **Comprehensive Base List**: Includes essential survival items for any disaster.
*   **Command-Line Interface**: Easy to use from your terminal.

## Installation

This utility is self-contained and written in Python 3.11. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/apocalypse-prep-checklist/` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

Run the script from the `src/` directory, specifying your desired scenario and location.

```bash
python src/checklist_generator.py --scenario <scenario_type> --location <location_type>
```

### Arguments

*   `--scenario`: (Optional) Specify the apocalypse scenario.
    *   Accepted values: `zombie`, `nuclear`, `ai_uprising`, `alien_invasion`, `climate_collapse`.
    *   Default: `default` (general preparedness).
*   `--location`: (Optional) Specify your location type.
    *   Accepted values: `urban`, `rural`, `coastal`, `mountain`.
    *   Default: `default` (general preparedness).

### Examples

**1. Default Checklist:**

```bash
python src/checklist_generator.py
```

**2. Zombie Apocalypse in an Urban Area:**

```bash
python src/checklist_generator.py --scenario zombie --location urban
```

**3. Nuclear Winter in a Rural Setting:**

```bash
python src/checklist_generator.py --scenario nuclear --location rural
```

**4. AI Uprising in a Mountainous Region:**

```bash
python src/checklist_generator.py --scenario ai_uprising --location mountain
```

## Development & Testing

To run the tests, navigate to the `utils/apocalypse-prep-checklist/` directory and execute the `test_checklist_generator.py` script using `unittest`:

```bash
python -m unittest tests/test_checklist_generator.py
```

All tests are deterministic and offline, using Python's `unittest.mock` to simulate command-line arguments and capture output.
