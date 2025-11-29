# Nightly Quantum Entanglement Linker

## Overview
The `Nightly Quantum Entanglement Linker` is a whimsical-yet-powerful utility designed to help you manage your digital entropy. It scans one or more specified directories for identical files, identifying 'entangled' duplicates that consume unnecessary disk space. Once identified, you can choose to simply report them, delete the redundant copies, or replace them with hardlinks to a single canonical file, effectively 'linking' their quantum states.

This tool is perfect for cleaning up project directories, download folders, or any location where files might have been copied multiple times.

## Features
- **Duplicate Detection**: Uses SHA256 hashing to reliably identify identical file content.
- **Flexible Scanning**: Scan one or multiple directories recursively.
- **Action Modes**: Choose between:
    - `report`: List all duplicate files found.
    - `delete`: Keep one instance of each duplicate set and delete the others.
    - `hardlink`: Keep one instance and replace all other duplicates with hardlinks pointing to the kept instance (saves disk space without losing access).

## Usage

### Prerequisites
- Python 3.6+ (tested with Python 3.11)

### Running the Utility
Navigate to the `utils/nightly-quantum-entanglement-linker/` directory and run `linker.py` with the desired arguments.

```bash
python src/linker.py --paths /path/to/dir1 /path/to/dir2 --action report
```

### Arguments
- `--paths <path1> [<path2> ...]`: **Required**. One or more paths to directories to scan for duplicates.
- `--action <mode>`: **Required**. The action to perform on identified duplicates. Choose from `report`, `delete`, or `hardlink`.

### Examples

**1. Report all duplicates in a single directory:**
```bash
python src/linker.py --paths ~/Downloads --action report
```

**2. Delete duplicate files across multiple project folders (keeping one copy):**
```bash
python src/linker.py --paths ~/Projects/ProjectA ~/Projects/ProjectB --action delete
```

**3. Replace duplicates with hardlinks in a specific archive directory:**
```bash
python src/linker.py --paths /mnt/archive/photos --action hardlink
```

## Important Notes
- **Hardlinking**: Be cautious when using the `hardlink` action. Hardlinks are only possible within the same filesystem. If duplicates span different filesystems, this action will fail for those specific files.
- **Deletion**: The `delete` action is irreversible. Always back up important data or use `report` mode first to review potential deletions.
- **Permissions**: Ensure the script has appropriate read/write permissions for the directories and files it needs to process.
