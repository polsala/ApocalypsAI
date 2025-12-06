# Nightly Echo-Chamber Auditor

## Purpose
The Nightly Echo-Chamber Auditor is a whimsical yet highly practical utility designed to help you declutter your digital spaces. It scans one or more specified directories, identifies files with identical content (echoes), and reports them. Optionally, it can even help you silence these echoes by deleting the duplicates.

## Features
- **Content-based Duplication Detection**: Uses MD5 hashing to ensure true content-based duplicate identification, not just name or size.
- **Recursive Scanning**: Dives deep into subdirectories to find all hidden echoes.
- **Flexible Reporting**: Outputs a clear list of duplicate files and their original counterparts.
- **Optional Deletion**: Safely removes duplicate files if the `--delete` flag is provided.

## Usage

```bash
python src/auditor.py <directory1> [directory2 ...] [--delete]
```

### Arguments
- `<directory1> [directory2 ...]`: One or more paths to directories to scan for duplicate files.
- `--delete`: (Optional) If provided, the utility will prompt for confirmation before deleting identified duplicate files. **Use with caution!**

### Examples

**1. Scan a single directory and report duplicates:**
```bash
python src/auditor.py ~/Downloads
```

**2. Scan multiple directories and report duplicates:**
```bash
python src/auditor.py ~/Documents /var/log/old_logs
```

**3. Scan a directory and delete duplicates (with confirmation):**
```bash
python src/auditor.py ~/MyPhotos --delete
```

## How it Works
1. The auditor traverses the specified directories, calculating an MD5 hash for each file's content.
2. It stores these hashes along with the file paths.
3. After scanning, it identifies all files that share the same hash but have different paths.
4. These are then reported as duplicates. If `--delete` is active, it will ask for confirmation before removing them, keeping the first encountered file as the 'original'.
