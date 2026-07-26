# Nightly Bit Rot Reclaimer

## Summary
This utility helps you identify files that might be considered 'bit rot' candidates – files that are old, large, or simply haven't been modified in a long time. It scans a specified directory (or the current one by default) and lists files that meet certain age or size criteria, suggesting them for review, archiving, or deletion to reclaim valuable digital space.

## Usage
```bash
./src/reclaimer.sh [OPTIONS]
```

### Options
- `--path <directory>`: The directory to scan. Defaults to the current directory (`.`).
- `--age <days>`: Files older than this many days (based on modification time) will be considered. Defaults to `365` days.
- `--size <MB>`: Files larger than this many megabytes will be considered. Defaults to `100` MB.
- `--dry-run`: (Optional) Only print the command that would be executed, without running `find`. Useful for debugging.
- `--help`: Display this help message.

## Examples

Scan the current directory for files older than 2 years or larger than 500MB:
```bash
./src/reclaimer.sh --age 730 --size 500
```

Scan a specific archive directory for files older than 90 days:
```bash
./src/reclaimer.sh --path /var/log/old_archives --age 90 --size 0 # size 0 means any non-empty file
```

Just see the `find` command that would run:
```bash
./src/reclaimer.sh --dry-run
```

## Output
The script will output a 'Reclamation Report' listing potential candidates with their size and last modification date. Each entry is prefixed with `[ ]` to suggest a manual review checkbox.

## Installation
Simply clone the repository and navigate to the `nightly-bit-rot-reclaimer` directory. The script is self-contained.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-bit-rot-reclaimer
chmod +x src/reclaimer.sh
```
