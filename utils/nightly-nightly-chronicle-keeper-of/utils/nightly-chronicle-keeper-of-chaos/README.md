# Nightly Chronicle Keeper of Chaos

## Overview

The `Nightly Chronicle Keeper of Chaos` is a whimsical-yet-useful utility designed to bring order to the post-apocalyptic digital landscape. It scans a specified directory and generates a concise Markdown summary, providing a snapshot of its contents. This includes the total number of files and directories, their cumulative size, and a highlight of the largest files, helping you quickly identify significant assets or potential resource hogs.

Think of it as your personal archivist, documenting the state of your digital rubble before the next wave of chaos (or a new feature release).

## Usage

To use the Chronicle Keeper, simply run the `chronicle_keeper.py` script with the path to the directory you wish to summarize.

```bash
python src/chronicle_keeper.py /path/to/your/directory
```

### Example Output

```markdown
# Chronicle of /path/to/your/directory

## Summary

- **Total Directories:** 5
- **Total Files:** 12
- **Total Size:** 1.2 MB

## Largest Files (Top 5)

- `important_data.db`: 500 KB
- `archive.zip`: 300 KB
- `logs/error.log`: 200 KB
- `docs/report.pdf`: 150 KB
- `src/main.py`: 50 KB
```

## Development

This utility is written in Python 3.11 and is self-contained. Tests are located in the `tests/` directory and can be run using `unittest`.
