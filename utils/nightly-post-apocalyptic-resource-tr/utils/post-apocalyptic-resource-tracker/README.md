# Post-Apocalyptic Resource Tracker

## Overview

In the grim darkness of the far future, or perhaps just next Tuesday, resources will be scarce. The `post-apocalyptic-resource-tracker` is a simple, self-contained command-line utility designed to help you keep tabs on your dwindling supplies. Whether it's cans of beans, purified water, or precious medical kits, this tool ensures you know exactly what you have left to survive another day.

## Features

*   **Add Resources**: Easily add new resources or increase the quantity of existing ones.
*   **Consume Resources**: Deduct resources as they are used, with checks to prevent over-consumption.
*   **List Resources**: Get a clear, up-to-date inventory of all your vital supplies.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Installation

This utility is designed to be run directly. Simply navigate to its directory:

```bash
cd utils/post-apocalyptic-resource-tracker/
```

## Usage

Run the `tracker.py` script with various commands:

```bash
python src/tracker.py --help
```

### Examples:

1.  **Add 10 units of 'Canned Beans':**
    ```bash
    python src/tracker.py add "Canned Beans" 10
    ```

2.  **Add 5 units of 'Purified Water':**
    ```bash
    python src/tracker.py add "Purified Water" 5
    ```

3.  **Consume 2 units of 'Canned Beans':**
    ```bash
    python src/tracker.py consume "Canned Beans" 2
    ```

4.  **List all current resources:**
    ```bash
    python src/tracker.py list
    ```

5.  **Attempt to consume more 'Purified Water' than available (e.g., 10 when only 5 exist):**
    ```bash
    python src/tracker.py consume "Purified Water" 10
    ```
    (This will output a warning and not change the quantity.)

## License

This project is licensed under the MIT License - see the `LICENSE` file in the repository root for details.
