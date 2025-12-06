# Post-Apocalyptic Resource Allocator

## Overview

In the grim darkness of the far future (or just next Tuesday), resources are scarce. The `post-apocalyptic-resource-allocator` is your trusty companion for ensuring your survival group has enough provisions to weather the storm. This CLI utility helps you calculate the total resources needed for your population over a specified duration and checks if your current scavenged supplies are sufficient.

## Features

*   Calculates total resource requirements (food, water, ammo, medical supplies).
*   Compares required resources against your current inventory.
*   Identifies resource shortfalls and surpluses.
*   Provides a clear, actionable report for your survival planning.

## Usage

Run the script from your terminal. You'll need to provide the number of survivors, the desired survival duration in days, and your current inventory of resources.

### Prerequisites

*   Python 3.8+

### Command Line Arguments

*   `--population <int>`: The number of survivors in your group. (Required)
*   `--duration-days <int>`: The number of days you plan to survive. (Required)
*   `--food <float>`: Current amount of food units available. (Default: 0.0)
*   `--water <float>`: Current amount of water units available. (Default: 0.0)
*   `--ammo <float>`: Current amount of ammunition units available. (Default: 0.0)
*   `--meds <float>`: Current amount of medical supply units available. (Default: 0.0)

### Example

```bash
python src/allocator.py --population 5 --duration-days 30 --food 500 --water 400 --ammo 100 --meds 20
```

## Default Consumption Rates (per person, per day)

*   **Food**: 2.0 units
*   **Water**: 3.0 units
*   **Ammo**: 0.1 units (represents occasional use/maintenance)
*   **Medical Supplies**: 0.05 units (represents minor injuries/preventative care)

These rates are hardcoded for simplicity but can be adjusted in the `src/allocator.py` file if your apocalypse has different metabolic or combat needs.

## Output Explanation

The utility will print a detailed report indicating:

*   Total required resources.
*   Your current inventory.
*   Any shortfalls or surpluses.
*   A final verdict on your survival prospects for the specified duration.
