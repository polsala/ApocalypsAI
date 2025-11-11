# Resource Scavenger: Prepare for Scarcity!

In the face of impending digital resource scarcity, the `resource-scavenger` utility helps you identify and reclaim valuable space within your repository. It scans a specified directory for files and folders that might be ripe for 'scavenging' – whether they're excessively large, suspiciously old, or simply empty.

Think of it as your pre-apocalyptic clean-up crew, ensuring your project is lean, efficient, and ready to survive any data crunch.

## Features

*   **Oversized File Detection**: Flags files exceeding a configurable size threshold.
*   **Ancient Artifact Identification**: Points out files not modified within a configurable number of days.
*   **Void Zone Discovery**: Locates and reports empty directories.

## Usage

Run the `scavenger.py` script from the `src` directory, providing the target path and optional thresholds.

```bash
python src/scavenger.py --path /path/to/your/repo \
                       --size-threshold-mb 10 \
                       --age-threshold-days 365
```

### Arguments

*   `--path <directory>` (required): The root directory to scan.
*   `--size-threshold-mb <int>` (optional, default: 50): Files larger than this (in MB) will be flagged.
*   `--age-threshold-days <int>` (optional, default: 365): Files not modified in this many days will be flagged.

## Example Output

```
--- Resource Scavenger Report ---

[OVERSIZED FILE] /path/to/your/repo/assets/huge_texture.png (75.2 MB)
[ANCIENT ARTIFACT] /path/to/your/repo/old_docs/legacy_spec.pdf (Last modified: 2020-01-15)
[VOID ZONE] /path/to/your/repo/empty_cache/
[OVERSIZED FILE] /path/to/your/repo/build/temp_archive.zip (120.1 MB)

--- Scavenging complete. Your repository is slightly less doomed. ---
```
