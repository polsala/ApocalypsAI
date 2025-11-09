# Digital Dust Bunny Sweeper

![Dust Bunny Icon](https://raw.githubusercontent.com/polsala/ApocalypsAI/main/.github/assets/dust_bunny.png) <!-- Placeholder for a future whimsical icon -->

## 🧹 What is it?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful command-line utility designed to help you declutter your digital workspace. It scours specified directories for 'dust bunnies' – old, forgotten files (like logs, temporary files, backups) and empty directories – and offers to sweep them away, freeing up valuable disk space and bringing a sense of order to your digital life.

Think of it as a tiny, diligent robot vacuum for your file system, but with more charm and less risk of getting stuck under the couch.

## ✨ Features

*   **Finds Old Files**: Identifies files older than a specified age with configurable extensions.
*   **Detects Empty Directories**: Locates and lists directories that contain no files or subdirectories.
*   **Dry Run Mode**: Preview what would be swept without making any changes.
*   **Interactive Confirmation**: Asks for your approval before deleting anything (unless forced).
*   **Configurable**: Adjust the age threshold and file extensions to target.
*   **Whimsical Output**: Enjoy charming messages as your system gets tidied up.

## 🚀 How to Use

### Prerequisites

*   Python 3.6+

### Installation (Standalone)

No installation needed! Just download the `dust_bunny_sweeper.py` script and run it directly.

```bash
cd utils/digital-dust-bunny-sweeper/src
python dust_bunny_sweeper.py --help
```

### Basic Usage

To scan your current directory for dust bunnies older than 30 days and with default extensions (`.log`, `.tmp`, `.bak`):

```bash
python dust_bunny_sweeper.py --path .
```

### Dry Run (Recommended First Step)

Always start with a dry run to see what the sweeper will do without actually deleting anything:

```bash
python dust_bunny_sweeper.py --path /path/to/clean --dry-run
```

### Sweeping with Custom Age and Extensions

To find files older than 60 days, including `.old` and `.cache` files, in your home directory:

```bash
python dust_bunny_sweeper.py --path ~/ --age 60 --extensions .log .tmp .old .cache
```

### Force Deletion (Use with Caution!)

To skip the interactive confirmation and delete immediately (useful for automation, but be careful!):

```bash
python dust_bunny_sweeper.py --path /path/to/logs --age 7 --extensions .log --force
```

### Command Line Arguments

*   `--path <directory>` (required): The root directory to start sweeping from.
*   `--age <days>` (optional, default: 30): Files older than this many days will be considered dust bunnies.
*   `--extensions <ext1> <ext2> ...` (optional, default: `.log`, `.tmp`, `.bak`): File extensions to target for deletion.
*   `--dry-run` (optional): Perform a scan and report, but do not delete any files or directories.
*   `--force` (optional): Skip interactive confirmation and proceed with deletion immediately.

## ⚠️ Important Notes

*   **Backup**: Always back up important data before running any file deletion utility.
*   **Permissions**: Ensure the script has appropriate read/write permissions for the directories it needs to sweep.
*   **Use with Care**: While designed to be safe, `--force` mode bypasses confirmation. Understand what you're deleting!

## 💖 Contributing

Got an idea for a new feature or a more whimsical message? Feel free to contribute to the ApocalypsAI project!
