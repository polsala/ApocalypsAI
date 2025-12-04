# Nightly File Deduplicator

A tiny, self‑contained tool that finds duplicate files in a directory tree and lets you either report, delete, or move the duplicates while keeping one copy.

## Features

* **Report** – Show a list of duplicate files grouped by SHA‑256 hash.
* **Delete** – Remove all but the first occurrence of each duplicate.
* **Move** – Move duplicate files to a target directory, keeping the first copy in place.
* **Dry‑run** – Preview actions without making any changes.

## Usage

```bash
# Report duplicates
python -m deduplicator --root /path/to/scan

# Delete duplicates (keep first copy)
python -m deduplicator --root /path/to/scan --action delete

# Move duplicates to /tmp/duplicates
python -m deduplicator --root /path/to/scan --action move --target-dir /tmp/duplicates

# Dry‑run delete
python -m deduplicator --root /path/to/scan --action delete --dry-run
```

## Installation

No installation is required – just copy the `utils/nightly-file-deduplicator` folder into your repository. The script uses only the Python standard library.

## Tests

Run the tests with:

```bash
python -m unittest discover utils/nightly-file-deduplicator/tests
```

The tests are deterministic and use temporary directories, so they can run offline.

---

> **Tip**: Use this tool as part of a nightly cleanup job to keep your repository or backup directories tidy.
