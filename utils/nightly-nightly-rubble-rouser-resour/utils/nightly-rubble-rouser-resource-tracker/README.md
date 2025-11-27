# Rubble-Rouser Resource Tracker

## Overview

The `nightly-rubble-rouser-resource-tracker` is a simple command-line utility designed to help survivors keep tabs on their precious scavenged resources. In a world where every can of beans and every spare battery counts, knowing what you have and where you're keeping it is crucial. This tool allows you to manage resources across different 'stashes' (e.g., 'Home Base', 'Abandoned Bunker', 'Supply Drop Alpha').

## Features

*   **Add Resources**: Easily log new findings to a specific stash.
*   **Remove Resources**: Deduct items when they're used or moved.
*   **List Stashes/Resources**: Get an overview of all your stashes or the contents of a single stash.
*   **Total Item Count**: Find out the total quantity of a specific item across all your locations.

## Usage

### Prerequisites

*   Python 3.6+

### Installation (Local)

1.  Navigate to the `utils/nightly-rubble-rouser-resource-tracker/` directory.
2.  Run the `tracker.py` script directly.

### Commands

The tracker uses a `resources.json` file in the same directory to store data. If it doesn't exist, it will be created automatically.

*   **Add an item to a stash:**
    ```bash
    python src/tracker.py add "Home Base" "Canned Beans" 5
    ```

*   **Remove an item from a stash:**
    ```bash
    python src/tracker.py remove "Home Base" "Canned Beans" 2
    ```

*   **List all resources in a specific stash:**
    ```bash
    python src/tracker.py list "Abandoned Bunker"
    ```

*   **List all stashes and their contents:**
    ```bash
    python src/tracker.py list
    ```

*   **Get the total quantity of an item across all stashes:**
    ```bash
    python src/tracker.py total "Water Bottle"
    ```

## Data Format (`resources.json`)

The data is stored in a simple JSON format:

```json
{
  "Home Base": {
    "Canned Beans": 3,
    "Water Bottle": 10
  },
  "Abandoned Bunker": {
    "First Aid Kit": 1,
    "Rope": 5
  }
}
```
