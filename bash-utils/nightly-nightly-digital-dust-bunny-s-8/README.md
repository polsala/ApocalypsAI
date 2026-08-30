# nightly-digital-dust-bunny-sweeper

A whimsical Bash script to identify and optionally sweep away digital dust bunnies (old, unused files) from specified directories. Keep your digital space tidy with a touch of charm!

## ✨ Features

- **Dust Bunny Detection**: Scans a target directory for files older than a specified number of days.
- **Whimsical Messaging**: Enjoy delightful messages as your system gets a digital spring clean.
- **Dry Run Mode**: By default, it just lists the dusty files without taking action.
- **Interactive Sweep**: Opt to be prompted before moving files to a temporary "Digital Dustbin".
- **Force Sweep**: Move files directly to the "Digital Dustbin" without confirmation.
- **Digital Dustbin**: Old files are moved to a unique timestamped directory in your home folder (`~/.digital_dustbin_YYYYMMDDHHMMSS`) for review, rather than immediate deletion.

## 🚀 Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS] [DIRECTORY]
```

### Options:

- `-d <days>`: Specify the age in days for files to be considered "dust bunnies" (default: `30`).
- `-s`: Enable **interactive sweep mode**. You'll be prompted to confirm before files are moved.
- `-f`: Enable **force sweep mode**. Files will be moved to the dustbin without any prompt.
- `-h`: Display the help message.

### Arguments:

- `DIRECTORY`: The path to the directory you want to scan (default: `~/Downloads`).

### Examples:

1. **Dry run (default behavior)**: List all files older than 30 days in `~/Downloads`.
   ```bash
   ./src/dust_bunny_sweeper.sh
   ```

2. **Scan a specific directory for files older than 60 days (dry run)**:
   ```bash
   ./src/dust_bunny_sweeper.sh -d 60 ~/Documents/old_projects
   ```

3. **Interactively sweep files older than 90 days in your home directory**:
   ```bash
   ./src/dust_bunny_sweeper.sh -d 90 -s ~
   ```

4. **Force sweep files older than 7 days in your temporary directory**:
   ```bash
   ./src/dust_bunny_sweeper.sh -d 7 -f /tmp
   ```

## 🧹 The Digital Dustbin

When files are swept, they are moved to a newly created directory like `~/.digital_dustbin_20231027143501`. This allows you to review the "dust bunnies" before deciding to permanently delete them. You are responsible for clearing out the dustbin when you're confident you no longer need the files.

## ⚠️ Important Notes

- The script uses `mv` to move files, not `rm` to delete them directly, providing a safety net.
- Always review the output, especially in dry run mode, before performing a sweep.
- Ensure you have appropriate permissions for the target directory and your home directory.
- Files with special characters in their names are handled safely.
