# Nightly Echo Chamber Purifier

## Purpose
This utility, the 'Nightly Echo Chamber Purifier', helps you identify and optionally remove duplicate files within a specified directory. It's designed to declutter your digital spaces, ensuring that redundant copies of files don't take up unnecessary storage or create confusion.

## How it Works
The purifier scans a target directory recursively, first grouping files by size for efficiency. Then, for groups with multiple files, it calculates SHA256 hashes for their content. Files with identical hashes are considered duplicates. It skips empty files as their content is trivial.

## Usage

```bash
python src/purifier.py <directory_path> [--delete]
```

- `<directory_path>`: The path to the directory you want to scan for duplicates.
- `--delete`: (Optional) If provided, the utility will automatically delete all but one instance of each set of duplicate files. **Use with extreme caution! Always back up important data before using the `--delete` flag.**

## Examples

### Scan for duplicates without deleting:
```bash
python src/purifier.py ./my_project_folder
```

### Scan and delete duplicates:
```bash
python src/purifier.py /var/log/old_backups --delete
```

## Output
The utility will print a list of identified duplicate groups, showing the original file (the first one found) and all its duplicates. If `--delete` is used, it will also report which files were removed.
