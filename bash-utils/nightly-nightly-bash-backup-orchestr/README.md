# Nightly Bash Backup Orchestrator

A whimsical-yet-useful Bash utility that orchestrates automated backups with configurable strategies, encryption, and whimsical status messages.

## Features

- **Multiple Backup Strategies**: Full, incremental, and differential backups
- **Encryption Support**: Optional GPG encryption for sensitive data
- **Whimsical Status Messages**: Because backups should be fun
- **Configurable Retention**: Automatic cleanup of old backups
- **Email Notifications**: Optional email alerts for backup status
- **Dry Run Mode**: Test your configuration before committing

## Installation

1. Clone or download this utility to your system
2. Make the script executable: `chmod +x src/backup_orchestrator.sh`
3. Configure your settings in `config/backup_config.conf`

## Usage

```bash
# Run a full backup
./src/backup_orchestrator.sh --strategy full

# Run an incremental backup
./src/backup_orchestrator.sh --strategy incremental

# Run a dry run to test configuration
./src/backup_orchestrator.sh --dry-run

# View help
./src/backup_orchestrator.sh --help
```

## Configuration

Edit `config/backup_config.conf` to customize:

- Source directories to backup
- Destination paths
- Encryption settings
- Retention policies
- Email notification settings

## Whimsical Messages

The orchestrator includes whimsical status messages to make your backup experience more delightful. Examples:

- "Backing up your digital treasures like a digital dragon guarding its hoard!"
- "Compressing files with the efficiency of a squirrel preparing for winter!"
- "Encrypting your data with the secrecy of a ninja in a library!"

## Requirements

- Bash 4.0+
- rsync
- tar
- gzip
- GPG (optional, for encryption)
- mailx or sendmail (optional, for email notifications)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter issues or have suggestions, please open an issue in the repository.
