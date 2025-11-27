# Temporal Tear Triage Tool

## Overview

In the chaotic aftermath of temporal anomalies, prioritizing tasks can be the difference between a stable timeline and utter paradox. The `Temporal Tear Triage Tool` is a whimsical-yet-useful command-line utility designed to help you manage and prioritize your "temporal anomalies" (tasks) based on their urgency and impact. Whether you're mending a fractured timeline or just organizing your daily chores, this tool ensures you tackle the most critical issues first.

## Features

*   **Add Anomalies**: Log new tasks with a description, urgency, and impact rating.
*   **Prioritize**: Automatically calculates a "Triage Score" to sort anomalies from most critical to least.
*   **Complete Anomalies**: Mark tasks as resolved, removing them from your active list.
*   **Persistence**: Saves and loads your anomaly list to a local JSON file, so your timeline remains consistent across sessions.

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed.

1.  Navigate to the `utils/temporal-tear-triage-tool/` directory.
2.  Run the script directly.

## Usage

```bash
python src/triage_tool.py --help
```

### Examples:

**1. Add a new temporal anomaly:**

```bash
python src/triage_tool.py add "Repair the Chrono-Flux Capacitor" --urgency 5 --impact 5
python src/triage_tool.py add "Retrieve misplaced spatiotemporal wrench" --urgency 3 --impact 4
python src/triage_tool.py add "Feed the time-displaced cat" --urgency 2 --impact 1
```

**2. List all active anomalies by priority:**

```bash
python src/triage_tool.py list
```

**3. Mark an anomaly as complete (by its ID):**

```bash
python src/triage_tool.py complete 1
```

(The ID is shown when you `list` anomalies.)

## Development

The tool uses a simple JSON file (`anomalies.json` by default) to store its data.
Tests are located in the `tests/` directory and can be run using `pytest`.

```bash
# From the temporal-tear-triage-tool directory
pytest tests/
```
