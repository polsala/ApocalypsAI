# Wasteland Resource Tracker

A whimsical-yet-useful command-line utility for tracking your vital resources in a post-apocalyptic world (or just your pantry). Keep tabs on your food, water, ammo, or any other critical supplies, set depletion alerts, and ensure you're always prepared for the next scavenging run or unexpected mutant encounter.

## Features

*   **Resource Management**: Add, remove, and update quantities of various resources.
*   **Critical Thresholds**: Define minimum safe levels for each resource.
*   **Alerts**: Get notified when a resource falls below its critical threshold.
*   **Persistence**: Your resource data is saved locally, so you don't lose track between sessions.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

1.  Navigate to the `utils/wasteland-resource-tracker/` directory.
2.  Run the `tracker.py` script directly.

## Usage

The `tracker.py` script supports several commands:

```bash
python src/tracker.py --help
```

### Examples:

**1. Initialize or view current resources:**
```bash
python src/tracker.py status
```

**2. Add a new resource:**
```bash
python src/tracker.py add --name "Canned Beans" --quantity 10 --threshold 3
```

**3. Consume a resource:**
```bash
python src/tracker.py consume --name "Canned Beans" --quantity 2
```

**4. Replenish a resource:**
```bash
python src/tracker.py replenish --name "Water Bottles" --quantity 5
```

**5. Update a resource's threshold:**
```bash
python src/tracker.py set-threshold --name "Water Bottles" --threshold 5
```

**6. Remove a resource:**
```bash
python src/tracker.py remove --name "Ammo .308"
```

## Data Storage

Resource data is stored in a `resources.json` file within the `src/` directory. This file is automatically created and managed by the utility.
