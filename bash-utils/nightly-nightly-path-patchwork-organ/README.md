# Nightly PATH Patchwork Organizer

A whimsical Bash utility to clean, deduplicate, and validate your `PATH` environment variable, ensuring a smoother journey through the digital wasteland.

## Overview

Over time, your shell's `PATH` can become a tangled mess of duplicate entries, non-existent directories, and suboptimal ordering. The `Nightly PATH Patchwork Organizer` helps you tidy up this crucial environmental variable, making your command-line experience more efficient and less prone to unexpected behavior.

It identifies:
- **Duplicate entries**: Paths that appear multiple times.
- **Non-existent directories**: Paths that no longer point to valid locations on your filesystem.

It can then output a cleaned `PATH` or provide an `export` command to apply the changes.

## Usage

```bash
./src/path_organizer.sh [OPTIONS]
```

### Options

- `--dry-run`: (Default) Shows the proposed cleaned `PATH` without generating an `export` command.
- `--apply`: Prints the `export PATH="..."` command to standard output. You can `eval` this command to apply the changes to your current shell session.
- `--help`: Displays this help message.

### Examples

1. **See what would be cleaned (dry run):**
   ```bash
   ./src/path_organizer.sh
   ```
   (This will use your current `PATH` environment variable)

2. **Apply the cleaned `PATH` to your current shell:**
   ```bash
   eval "$(./src/path_organizer.sh --apply)"
   ```
   **Caution**: Always review the output of `--dry-run` before using `--apply` with `eval`.

3. **Clean a specific `PATH` string (for scripting or testing):**
   ```bash
   CLEANED_PATH=$(PATH="/usr/local/bin:/usr/bin:/usr/local/bin:/nonexistent/path" ./src/path_organizer.sh --dry-run)
   echo "$CLEANED_PATH"
   ```

## How it Works

The script splits your `PATH` into individual components, then iterates through them. For each component, it checks if the directory exists and if it has already been added to the new, cleaned `PATH`. It then reconstructs the `PATH` with only unique, existing entries, preserving the original order of the *first occurrence* of each valid path.

## Installation

Simply clone the `ApocalypsAI` repository and navigate to this utility's directory:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-path-patchwork-organizer
```

The script is self-contained and requires no external dependencies beyond standard Bash utilities.

## Tests

To run the automated tests:

```bash
./tests/test_path_organizer.sh
```
