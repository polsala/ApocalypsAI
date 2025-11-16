# Nightly Rubble-Rouser Resource Tracker

## Overview

In the desolate aftermath, every scrap counts! The `nightly-rubble-rouser-resource-tracker` is a simple, command-line utility designed to help survivors keep tabs on their scavenged resources. Whether it's purified water, canned goods, or precious scrap metal, this tool ensures you know exactly what you have, where you have it (conceptually!), and how much.

It stores your inventory in a local JSON file, making it easy to manage and review your vital supplies.

## Features

*   **Add Resources**: Increment the quantity of an existing resource or add a new one.
*   **Remove Resources**: Decrement the quantity of a resource. If the quantity drops to zero or below, the resource is removed from the inventory.
*   **Set Resources**: Directly set the quantity of a resource.
*   **List Inventory**: Display all tracked resources and their current quantities.
*   **Persistent Storage**: All data is saved to a `resources.json` file in the utility's directory.

## Installation & Usage

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/nightly-rubble-rouser-resource-tracker
    ```
2.  **Run**: Execute the `tracker.py` script with the desired command.

### Commands:

*   **Add a resource**: `python src/tracker.py add <resource_name> <quantity>`
    ```bash
    python src/tracker.py add water 5
    python src/tracker.py add canned_beans 3
    ```

*   **Remove a resource**: `python src/tracker.py remove <resource_name> <quantity>`
    ```bash
    python src/tracker.py remove water 2
    ```

*   **Set a resource quantity**: `python src/tracker.py set <resource_name> <quantity>`
    ```bash
    python src/tracker.py set medical_kits 1
    ```

*   **List all resources**: `python src/tracker.py list`
    ```bash
    python src/tracker.py list
    ```

## Example Workflow

```bash
# Initial setup (optional, file will be created on first save)
# python src/tracker.py set water 10
# python src/tracker.py set food_rations 5

# Add some newly scavenged items
python src/tracker.py add water 3
python src/tracker.py add scrap_metal 15

# Consume some food
python src/tracker.py remove food_rations 1

# Check current inventory
python src/tracker.py list

# Output might look like:
# Current Resources:
#   food_rations: 4
#   scrap_metal: 15
#   water: 13
```
