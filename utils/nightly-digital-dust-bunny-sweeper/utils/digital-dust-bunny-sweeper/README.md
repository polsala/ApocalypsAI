# Digital Dust Bunny Sweeper

Tired of digital clutter accumulating in your repository? The ApocalypsAI Digital Dust Bunny Sweeper is here to help! This whimsical utility identifies and helps you clean up empty directories and ancient, forgotten files (like temporary logs or backup remnants) that are just taking up space and slowing down your post-apocalyptic build times. Keep your digital bunker tidy!

## Features

*   **Empty Directory Detection**: Finds and lists directories that contain no files or subdirectories.
*   **Old File Identification**: Locates files matching specified patterns (e.g., `*.log`, `*.tmp`, `*.bak`) that are older than a configurable age.
*   **Dry Run Mode**: Safely preview what would be cleaned without making any changes.

## Usage

Run the utility from your repository root or any specified path:

```bash
python src/sweeper.py <path_to_scan> [--dry-run] [--age <days>] [--patterns <pattern1> <pattern2> ...]
```

### Arguments

*   `<path_to_scan>`: The root directory to start scanning from (e.g., `.` for current directory).
*   `--dry-run`: (Optional) If present, the utility will only print what it *would* clean, without actually deleting anything. Highly recommended for initial runs.
*   `--age <days>`: (Optional) The minimum age in days for a file to be considered 'old'. Defaults to `30` days. Only applies to files matching patterns.
*   `--patterns <pattern1> <pattern2> ...`: (Optional) One or more glob patterns (e.g., `*.log`, `*.tmp`, `*.bak`) to identify files that might be 'dust bunnies'. Defaults to `['*.log', '*.tmp', '*.bak', '*.old', '*.swp']`.

### Examples

Scan the current directory for empty folders and `.log` files older than 60 days, in dry-run mode:

```bash
python src/sweeper.py . --dry-run --age 60 --patterns "*.log"
```

Scan a specific build output directory for any default 'dust bunny' files older than 7 days:

```bash
python src/sweeper.py ./build_output --age 7
```
