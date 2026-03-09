# Nightly Digital Dust Bunny Sweeper

## Summary
This utility helps you identify and manage digital clutter by scanning specified directories for files that are both old and large. It metaphorically labels these files as 'digital dust bunnies' that might be candidates for archival or deletion, helping you reclaim precious storage space.

## Usage

```bash
node src/index.js <directory_path> [--age <days>] [--size <MB>]
```

### Arguments
- `<directory_path>`: The path to the directory you want to scan for digital dust bunnies. This is a required argument.

### Options
- `--age <days>`: The minimum age in days for a file to be considered a 'dust bunny'. Files last modified older than this many days will be flagged. Defaults to `365` days (1 year).
- `--size <MB>`: The minimum size in megabytes for a file to be considered a 'dust bunny'. Files larger than this size will be flagged. Defaults to `100` MB.

## Examples

Scan your 'downloads' folder for files older than 2 years and larger than 500MB:
```bash
node src/index.js ~/Downloads --age 730 --size 500
```

Scan your entire home directory with default thresholds (1 year, 100MB):
```bash
node src/index.js ~/
```

## Installation

1. Navigate to the `node-utils/nightly-digital-dust-bunny-sweeper` directory.
2. Ensure you have Node.js installed.
3. Run the utility directly:
   ```bash
   node src/index.js /path/to/scan
   ```
