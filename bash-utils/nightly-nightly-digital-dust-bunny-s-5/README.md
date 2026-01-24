# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful Bash utility designed to help you keep your digital environment tidy. It scans specified directories for old, unused files and directories – affectionately termed "digital dust bunnies" – and offers to sweep them away. Think of it as a friendly janitor for your filesystem, preventing digital clutter from accumulating.

This utility is perfect for cleaning up:
- Old downloads
- Temporary files
- Cache directories
- Any other specified paths where digital debris might gather.

## ✨ Features

- **Whimsical Interface**: Presents old files as "digital dust bunnies."
- **Configurable Paths**: Scan default common locations or specify your own.
- **Age Threshold**: Define how old a file or directory must be to be considered a "dust bunny."
- **Dry Run Mode**: Preview what would be deleted without actually removing anything.
- **Interactive Deletion**: Prompts for confirmation before sweeping.
- **Auto-Confirm Option**: For automated cleanups (use with caution!).

## 🚀 Usage

### Prerequisites

- Bash (version 4.0 or higher recommended)
- `find` utility
- `rm` utility

### Basic Scan (Dry Run)

To see what digital dust bunnies are lurking in your default locations (e.g., `~/Downloads`, `/tmp`, `~/.cache`, `/var/tmp`) without deleting anything, run:

```bash
./src/dust_bunny_sweeper.sh -d
```

### Scan Specific Paths

To scan a specific directory (e.g., `/var/log/old_logs`) and look for files older than 60 days:

```bash
./src/dust_bunny_sweeper.sh -p /var/log/old_logs -a 60 -d
```

You can specify multiple paths:

```bash
./src/dust_bunny_sweeper.sh -p /path/to/downloads -p /path/to/temp -a 90 -d
```

### Interactive Sweep

To perform an interactive sweep of default locations, prompting for confirmation before deletion:

```bash
./src/dust_bunny_sweeper.sh
```

### Automated Sweep (Use with Caution!)

To automatically sweep away dust bunnies older than 30 days in default locations without prompting:

```bash
./src/dust_bunny_sweeper.sh -y
```

**WARNING**: Using `-y` will delete files without confirmation. Ensure you understand the implications before using this option in automated scripts.

### Full Options

```
Usage: ./src/dust_bunny_sweeper.sh [-p <path>] [-a <days>] [-d] [-y] [-h]
  -p <path>  : Add a path to scan (can be used multiple times). Defaults to common locations.
  -a <days>  : Age threshold in days. Files/dirs older than this are 'dust bunnies'. Default: 30.
  -d         : Dry run mode. Only list 'dust bunnies', do not delete. (Default: false)
  -y         : Auto-confirm deletion without prompt. USE WITH CAUTION! (Default: false)
  -h         : Display this help message.
```

## 🧪 Testing

The utility includes a self-contained test script that uses mocks to ensure deterministic and offline execution.

To run the tests:

```bash
./tests/test_dust_bunny_sweeper.sh
```

The tests will:
- Create a temporary directory for test artifacts.
- Mock `find`, `rm`, and `date` commands to control their behavior and prevent actual filesystem changes.
- Simulate various scenarios: no dust bunnies, dry run, interactive deletion (confirm/deny), and auto-confirmed deletion.
- Verify the script's output and exit codes.

## 🤝 Contributing

Feel free to suggest improvements, report bugs, or contribute to making the digital world a cleaner place!
