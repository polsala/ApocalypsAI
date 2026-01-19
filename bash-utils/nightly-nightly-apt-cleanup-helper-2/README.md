# nightly-apt-cleanup-helper

## Summary
A whimsical Bash utility that audits and safely cleans up unused APT packages, offering a post‑apocalypse system tidying report.

## Usage
```bash
./src/cleanup.sh [-n] <data-dir>
```
- `-n` : dry‑run (default). Shows what would be removed.
- `<data-dir>` : directory containing mock APT data files:
  - `installed.txt` – list of installed packages (one per line)
  - `auto_remove.txt` – list of packages that are auto‑removable

The script prints a colorful report and, unless `-n` is given, simulates removal by deleting entries from `installed.txt`.

## Example
```bash
mkdir mock-data
echo -e "libc6\nlinux-image-5.4.0-42-generic\nvim" > mock-data/installed.txt
echo "linux-image-5.4.0-42-generic" > mock-data/auto_remove.txt
./src/cleanup.sh mock-data
```

## License
MIT
