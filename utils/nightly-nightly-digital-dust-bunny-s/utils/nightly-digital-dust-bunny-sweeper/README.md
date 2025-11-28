# Nightly Digital Dust Bunny Sweeper

## 🧹 What it does

The Nightly Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to keep your file system pristine. It recursively scans a specified directory (or the current one by default) for empty folders and, like a diligent digital housekeeper, removes them. Say goodbye to those forgotten, hollow directories cluttering your workspace!

## ✨ Features

*   **Recursive Cleaning**: Traverses directory trees from the bottom up to ensure all empty subdirectories are caught.
*   **Dry Run Mode**: Preview which directories would be removed without actually deleting anything.
*   **Safe**: Will not remove the root directory you specify, even if it becomes empty after its children are swept away.
*   **Error Handling**: Gracefully handles permissions issues or other OS errors during directory listing or removal.

## 🚀 How to use

1.  **Navigate** to the `utils/nightly-digital-dust-bunny-sweeper/` directory.
2.  **Run** the `sweeper.py` script.

### Basic Usage

To clean empty directories in the current working directory:

```bash
python src/sweeper.py
```

### Specify a Root Directory

To clean empty directories starting from a specific path (e.g., `/path/to/your/project`):

```bash
python src/sweeper.py /path/to/your/project
```

### Dry Run (Recommended First!)

To see which directories *would* be removed without actually deleting them:

```bash
python src/sweeper.py --dry-run
```

Or for a specific path:

```bash
python src/sweeper.py /path/to/your/project --dry-run
```

## 🧪 Running Tests

To ensure the sweeper is working as expected, you can run its self-contained tests:

1.  **Navigate** to the `utils/nightly-digital-dust-bunny-sweeper/` directory.
2.  **Run** the test script:

```bash
python -m unittest tests/test_sweeper.py
```
