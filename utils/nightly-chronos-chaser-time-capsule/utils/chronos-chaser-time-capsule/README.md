# Chronos-Chaser Time Capsule Creator

## Overview

The 'Chronos-Chaser Time Capsule Creator' is a whimsical yet essential utility designed to help you preserve critical data before the inevitable. It takes a list of files and directories, bundles them into a timestamped `.zip` archive, and includes a `manifest.json` detailing the original paths, archived names, sizes, and MD5 hashes of all included items. Think of it as a digital emergency kit, ready for when time itself starts to unravel.

## Features

*   **Timestamped Archives**: Each time capsule is named with the creation date and time, ensuring unique and chronological preservation.
*   **Comprehensive Manifest**: A `manifest.json` file within each capsule records the original paths, archived names, sizes, and MD5 hashes of all included items.
*   **Self-Contained**: Everything you need is bundled into a single `.zip` file.
*   **Easy to Use**: Simple command-line interface.

## Usage

```bash
python src/time_capsule.py <path_to_item_1> [path_to_item_2] ... [path_to_item_N]
```

**Example:**

To create a time capsule containing `my_important_doc.txt` and the entire `config_files/` directory:

```bash
python src/time_capsule.py my_important_doc.txt config_files/
```

This will generate a file like `time_capsule_20231027_143000.zip` in the current directory (or the directory from which the script is run).

## Development

### Requirements

*   Python 3.8+

### Running Tests

```bash
python -m unittest tests/test_time_capsule.py
```
