# Nightly Bash Backup Buddy

A whimsical yet practical Bash utility for creating timestamped backups of directories with optional compression and automatic cleanup of old backups.

## Features

- Create timestamped backups of any directory
- Optional compression using tar and gzip
- Automatic cleanup of old backups (configurable retention)
- Whimsical ASCII art and progress messages
- Dry-run mode for testing
- Cross-platform compatibility (Linux, macOS, WSL)

## Usage

```bash
# Basic backup
./src/main.sh /path/to/source /path/to/backup/location

# Compressed backup with custom retention
./src/main.sh --compress --retention 7 /path/to/source /path/to/backup/location

# Dry run to see what would happen
./src/main.sh --dry-run /path/to/source /path/to/backup/location

# Help
./src/main.sh --help
```

## Options

- `--compress`: Create compressed tar.gz backups
- `--retention N`: Keep only the last N backups (default: 5)
- `--dry-run`: Show what would be done without actually doing it
- `--help`: Display help message

## Examples

```bash
# Create a compressed backup with 10-day retention
./src/main.sh --compress --retention 10 ~/Documents /backups

# Create an uncompressed backup
./src/main.sh ~/Projects /backups

# Dry run to preview
./src/main.sh --dry-run --compress ~/Documents /backups
```

## Requirements

- Bash 4.0+
- tar (for compression)
- gzip (for compression)
- date command

## License

MIT - feel free to backup your world!
