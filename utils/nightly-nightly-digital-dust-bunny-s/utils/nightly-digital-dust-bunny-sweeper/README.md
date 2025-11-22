# Nightly Digital Dust Bunny Sweeper

## 🧹 Purging the Digital Detritus

In the vast, ever-expanding digital landscape, empty directories can accumulate like forgotten dust bunnies under the server racks. They don't do much harm, but they certainly don't spark joy! The ApocalypsAI Nightly Digital Dust Bunny Sweeper is here to bring order to the chaos, recursively seeking out and eliminating these digital voids.

This utility is designed to help maintain a clean and organized file system, making navigation easier and reducing visual clutter. It's particularly useful for development environments, build outputs, or any directory structure that frequently generates and then discards temporary folders.

## ✨ Features

*   **Recursive Cleaning**: Traverses directory trees from the bottom up, ensuring nested empty folders are handled correctly.
*   **Dry-Run Mode**: Safely preview which directories would be deleted without making any actual changes.
*   **Simple & Self-Contained**: A single Python script with no external dependencies, easy to integrate and run.

## 🚀 Usage

To run the Digital Dust Bunny Sweeper, navigate to the `utils/nightly-digital-dust-bunny-sweeper` directory and execute the `sweeper.py` script.

```bash
python3 src/sweeper.py <path_to_directory_to_clean> [--dry-run]
```

### Arguments:

*   `<path_to_directory_to_clean>`: The root directory from which the sweeper will start its search for empty folders.
*   `--dry-run`: (Optional) If provided, the script will only report which directories *would* be deleted, without actually removing them. This is highly recommended for a first run!

### Examples:

**1. Dry-run to see what would be cleaned in your current directory:**

```bash
python3 src/sweeper.py . --dry-run
```

**2. Clean empty directories in a specific project folder:**

```bash
python3 src/sweeper.py /path/to/your/project/output
```

**3. Clean empty directories in the entire repository (use with caution!):**

```bash
python3 src/sweeper.py ../../ --dry-run
```

## 🧪 Testing

To ensure the sweeper is always ready for action, run its self-contained tests:

```bash
python3 -m unittest tests/test_sweeper.py
```
