# Apocalypse Prep Checklist

## Overview

The `apocalypse-prep-checklist` utility helps you prepare for the inevitable by generating a tailored survival checklist based on various doomsday scenarios. Whether you're bracing for a zombie horde, an AI uprising, or a rogue meteor, this tool provides a quick, actionable list of essentials.

## Usage

Run the script from the `src/` directory, specifying your chosen scenario using the `--scenario` flag.

```bash
python src/checklist.py --scenario <scenario_name>
```

### Examples

To get a checklist for a zombie apocalypse:

```bash
python src/checklist.py --scenario zombie
```

To prepare for an AI uprising:

```bash
python src/checklist.py --scenario ai-uprising
```

To see the general preparedness list:

```bash
python src/checklist.py --scenario general
```

## Supported Scenarios

*   `zombie`: Focuses on immediate survival, evasion, and basic needs.
*   `ai-uprising`: Emphasizes EMP protection, offline resources, and analog communication.
*   `meteor-strike`: Covers long-term survival in potentially harsh environments, shelter, and resource management.
*   `solar-flare`: Similar to AI, but focused on grid collapse and electronic disruption.
*   `general`: A foundational checklist for any unforeseen disaster.

## Installation

This utility is self-contained and requires Python 3.6+ (or compatible). No external dependencies are needed.

```bash
cd utils/apocalypse-prep-checklist/
python src/checklist.py --scenario general
```
