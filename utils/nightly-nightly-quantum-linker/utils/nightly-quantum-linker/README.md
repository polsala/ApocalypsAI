# Nightly Quantum Linker

## 🌌 Entangle Your Files, Save Your Space 🌌

The Nightly Quantum Linker is a whimsical-yet-powerful utility designed to help you reclaim precious disk space by identifying duplicate files within a specified directory and replacing them with hard links. Think of it as creating quantum entanglement between identical files – they appear in multiple places, but only one copy truly exists on the disk.

### How it Works

1.  **Scan**: It recursively traverses a target directory.
2.  **Hash**: For each file, it calculates a cryptographic hash (SHA256) to uniquely identify its content.
3.  **Identify Duplicates**: Files with identical hashes are considered duplicates.
4.  **Link**: For each set of duplicates, it keeps one original file and replaces all other identical copies with hard links pointing to that original. Hard links are file system entries that point to the same underlying data blocks on disk, meaning they consume no additional space for the file content.

### Features

*   **Space Saving**: Significantly reduces disk usage by eliminating redundant file data.
*   **Content Integrity**: Uses SHA256 hashing to ensure only truly identical files are linked.
*   **Dry Run Mode**: Preview the changes before committing them to your file system.
*   **Whimsical Naming**: Because even apocalypse prep needs a touch of magic.

### Usage

```bash
python src/linker.py --dir /path/to/your/directory [--dry-run]
```

*   `--dir <path>`: The root directory to scan for duplicate files.
*   `--dry-run`: (Optional) If specified, the utility will only report what it *would* do without making any changes to the file system. Highly recommended for a first run!

### Example

```bash
# See what would happen
python src/linker.py --dir ~/my_apocalypse_backups --dry-run

# Actually link the duplicates
python src/linker.py --dir ~/my_apocalypse_backups
```

### Installation

This utility is self-contained and requires Python 3.6+.

```bash
# No special installation needed, just run the script directly.
cd utils/nightly-quantum-linker
python src/linker.py --help
```

### Caveats

*   **Hard Links Only**: This utility creates hard links, which work only within the same file system partition. They cannot span across different partitions or network drives.
*   **Permissions**: Ensure the script has appropriate read/write permissions for the target directory.
*   **Backup**: While hard linking is generally safe, it's always wise to have backups before running any file system modification utility.
