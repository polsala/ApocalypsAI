# Cosmic Dust Bunny Collector

## 🌌🧹 Sweep Away the Void!

In the vast expanse of your repository, 'cosmic dust bunnies' — empty directories — can accumulate, cluttering your space like forgotten nebulae. The **Cosmic Dust Bunny Collector** is here to help you tidy up!

This utility scans a specified directory for any empty subdirectories and provides options to list them or gracefully remove them, ensuring your project remains as pristine as a freshly-formed galaxy.

## ✨ Features

*   **Find Empty Directories**: Recursively scans a path to identify all empty folders.
*   **Safe Listing**: Preview which directories would be removed before taking action.
*   **Efficient Cleanup**: Optionally remove identified empty directories.

## 🚀 Usage

### Prerequisites

*   Python 3.6+

### Installation (for standalone use)

No installation needed! Just place the `cosmic-dust-bunny-collector` folder anywhere and run the `collector.py` script.

### Running the Collector

```bash
# Navigate to the utility's source directory
cd utils/cosmic-dust-bunny-collector/src

# To list empty directories in the current working directory (or a specified path):
python collector.py --path ../../ --list

# To remove empty directories in the current working directory (or a specified path):
# BE CAREFUL! This will delete directories.
python collector.py --path ../../ --remove

# To get help:
python collector.py --help
```

**Note**: When using `--remove`, the script will attempt to delete directories. Ensure you have the necessary permissions and understand the implications.

## 🧪 Testing

To run the tests for this utility:

```bash
# Navigate to the utility's root directory
cd utils/cosmic-dust-bunny-collector/

# Run pytest (install if you don't have it: pip install pytest)
python -m pytest tests/
```
