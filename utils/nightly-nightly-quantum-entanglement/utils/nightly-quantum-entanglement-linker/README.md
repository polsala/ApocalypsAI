# Nightly Quantum Entanglement Linker

## 🌌 Overview

The `Nightly Quantum Entanglement Linker` is a whimsical-yet-powerful utility designed to bring order to the chaotic quantum foam of your file system. It scans a specified directory for identical files (duplicates) and, through a process akin to quantum entanglement, replaces all but one instance with hard links. This saves significant disk space and reduces redundancy, ensuring your repository remains lean and efficient, ready for the next cosmic event.

Think of it as collapsing the wave function of your data, making all identical particles share the same underlying reality on disk.

## ✨ Features

*   **Duplicate Detection**: Scans a target directory and its subdirectories to identify files with identical content using SHA256 hashing.
*   **Space Optimization**: Replaces duplicate files with hard links, pointing them all to a single physical file on disk.
*   **Non-Destructive Master**: The first encountered instance of a file content is preserved as the "master" link target.
*   **Detailed Reporting**: Provides a summary of linked files and the total disk space saved.
*   **Self-Contained**: Written in Python 3.11, with minimal dependencies, making it easy to run anywhere.

## 🚀 Usage

To unleash the power of quantum entanglement on your files, simply run the `linker.py` script with the target directory as an argument:

```bash
python src/linker.py /path/to/your/directory
```

Replace `/path/to/your/directory` with the actual path you wish to scan and optimize.

### Example:

```bash
# Scan and link duplicates in the current directory
python src/linker.py .

# Scan and link duplicates in a specific project folder
python src/linker.py ~/projects/my_apocalypse_bunker
```

## 🛠️ Development & Testing

The utility is written in Python 3.11.

### Dependencies

*   Python 3.11+ (standard library only)

### Running Tests

To ensure the quantum entanglement is stable and deterministic, run the provided unit tests:

```bash
python -m unittest tests/test_linker.py
```

The tests use `unittest.mock` to simulate file system operations, ensuring they are deterministic and do not modify your actual files.
