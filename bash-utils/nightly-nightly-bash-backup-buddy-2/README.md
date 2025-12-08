# Nightly Bash Backup Buddy

A whimsical yet practical Bash utility that creates timestamped backups of directories with fun messages and validates archives. Perfect for automated workflows and manual use.

## Features
- Creates timestamped backup archives
- Validates archives after creation
- Provides whimsical status messages
- Supports dry-run mode
- Configurable compression level

## Usage

```bash
# Basic backup
./src/main.sh /path/to/source /path/to/backup

# With options
./src/main.sh --dry-run --compress 9 /path/to/source /path/to/backup

# Help
./src/main.sh --help
```

## Installation

1. Clone or download this utility
2. Make the script executable: `chmod +x src/main.sh`
3. Run or integrate into your backup workflows

## Requirements
- Bash 4.0+
- tar
- gzip
- sha256sum

## License
MIT
