# nightly-disk-space-guardian

## Overview

`nightly-disk-space-guardian` is a tiny Bash utility that walks through a given directory, finds files larger than a user‑specified size, and prints a friendly report.  For the truly adventurous, it can also *move* those oversized files into a hidden `.trash` folder inside the target directory, keeping your workspace tidy while preserving the data.

## Features

- Scan any directory recursively.
- Size threshold expressed in megabytes.
- Optional `-m` flag to move oversized files to `<directory>/.trash`.
- Human‑readable size output using `numfmt`.
- Zero external dependencies – just Bash and core GNU utilities.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-disk-space-guardian
# Make the script executable
chmod +x src/disk_guardian.sh
```

You can also add the script to your `$PATH` for convenient global use.

## Usage

```bash
./src/disk_guardian.sh -d <directory> -s <size_mb> [-m]
```

- `-d <directory>` – Directory to scan (required).
- `-s <size_mb>` – Size threshold in megabytes (required).
- `-m` – If present, move each oversized file to `<directory>/.trash`.

### Examples

```bash
# Find files larger than 100 MB in the current folder
./src/disk_guardian.sh -d . -s 100

# Same scan, but automatically move the offenders to .trash
./src/disk_guardian.sh -d . -s 100 -m
```

## Testing

The utility ships with a Bash test suite that runs in a temporary sandbox.  To execute the tests:

```bash
cd tests
bash test_disk_guardian.sh
```

All tests should pass on any Unix‑like system with Bash, `dd`, `find`, `stat`, and `numfmt` available.

## License

MIT © ApocalypsAI community
