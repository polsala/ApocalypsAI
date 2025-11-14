# Digital Dust Bunny Sweeper

## Overview

In the grand scheme of impending apocalypses, digital clutter might seem trivial. Yet, a clean system is a resilient system! The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you maintain a tidy digital environment by identifying and optionally removing:

*   **Empty Directories**: Those forgotten folders that serve no purpose, like abandoned bunkers.
*   **Old, Unused Files**: Stale logs, temporary files, and backups that have long outlived their usefulness, akin to pre-collapse propaganda.

Think of it as preparing your digital bunker for the long haul, ensuring no unnecessary detritus weighs down your systems when the real chaos begins. A clean system is a happy (and less prone to crashing) system!

## Usage

### Prerequisites

*   Python 3.6+

### Running the Sweeper

Navigate to the `src` directory and run `sweeper.py`.

```bash
cd utils/digital-dust-bunny-sweeper/src
python sweeper.py --help
```

```
usage: sweeper.py [-h] [--paths PATHS [PATHS ...]] [--age AGE] [--extensions EXTENSIONS [EXTENSIONS ...]] [--delete]

Digital Dust Bunny Sweeper: Clean up digital detritus.

options:
  -h, --help            show this help message and exit
  --paths PATHS [PATHS ...]
                        One or more paths to scan (default: current directory).
  --age AGE             Files older than this many days will be considered old (default: 30).
  --extensions EXTENSIONS [EXTENSIONS ...]
                        File extensions to consider for 'old file' cleanup (e.g., .log .tmp .bak). Default: .log .tmp .bak
  --delete              Actually delete identified empty directories and old files. Use with caution!
```

**Example: Scan current directory for old logs and empty folders (dry run)**

```bash
python sweeper.py
```

**Example: Scan specific directories, considering files older than 60 days, and delete them**

```bash
python sweeper.py --paths /var/log /tmp --age 60 --extensions .log .temp --delete
```

## Development

### Testing

Tests are located in the `tests/` directory. To run them:

```bash
cd utils/digital-dust-bunny-sweeper
python -m unittest discover tests
```
