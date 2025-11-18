# Nightly Resource Scavenger Log

## Overview

The `nightly-resource-scavenger-log` is a simple command-line utility designed to help survivors (or just very organized preppers) keep track of their scavenged resources across various stash locations. In a world where every can of beans and roll of duct tape counts, knowing what you have and where it is can be the difference between thriving and... well, not thriving.

This tool allows you to:

*   **Add** new resources to a location.
*   **Remove** resources from a location.
*   **List** all resources, or resources specific to a location.

All data is stored locally in a JSON file, making it self-contained and easy to manage.

## Usage

### Prerequisites

*   Python 3.6+ (tested with Python 3.11)

### Running the Utility

Navigate to the `src` directory and run the `scavenger_log.py` script with the desired commands.

```bash
cd utils/nightly-resource-scavenger-log/src
python scavenger_log.py --help
```

### Commands

#### Add a resource

```bash
python scavenger_log.py add --item "Canned Beans" --quantity 5 --location "Kitchen Stash"
```

#### Remove a resource

```bash
python scavenger_log.py remove --item "Canned Beans" --quantity 2 --location "Kitchen Stash"
```

#### List all resources

```bash
python scavenger_log.py list
```

#### List resources by location

```bash
python scavenger_log.py list --location "Garage Cache"
```

## Data Storage

The utility stores its data in a JSON file named `scavenger_log.json` in the same directory as the `scavenger_log.py` script. This file is automatically created if it doesn't exist.

## Development & Testing

To run the tests, navigate to the `tests` directory and use `unittest`:

```bash
cd utils/nightly-resource-scavenger-log/tests
python -m unittest test_scavenger_log.py
```
