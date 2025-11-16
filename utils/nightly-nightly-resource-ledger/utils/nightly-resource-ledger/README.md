# Nightly Resource Ledger

A simple, command-line utility for tracking your scavenged resources in the post-apocalyptic wasteland. Keep tabs on what you have, where you found it, and how much is left before the next horde arrives.

## Features

*   **Add Resources**: Log new finds with quantity and optional location.
*   **Remove Resources**: Decrement quantities when resources are consumed or lost.
*   **List All Resources**: See your entire inventory at a glance.
*   **Show Specific Resource**: Check the total quantity of a particular item.

## Usage

The ledger stores its data in a `resources.json` file in the current working directory.

```bash
# Add 5 cans of "Canned Beans" found at "Old Supermarket"
python src/ledger.py add "Canned Beans" 5 --location "Old Supermarket"

# Add 1 "Duct Tape"
python src/ledger.py add "Duct Tape" 1

# Remove 2 "Canned Beans" (consumed)
python src/ledger.py remove "Canned Beans" 2

# List all current resources
python src/ledger.py list

# Show total quantity of "Canned Beans"
python src/ledger.py show "Canned Beans"
```

## Development

To run tests:

```bash
python -m unittest tests/test_ledger.py
```
