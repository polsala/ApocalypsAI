# Nightly Digital Dust Bunny Sweeper

## Summary
This whimsical utility helps you keep your digital realm tidy by identifying and sweeping away 'digital dust bunnies' – old, forgotten files and empty directories that clutter your filesystem.

## How it Works
The `dust_bunny_sweeper.sh` script scans a specified directory (or the current one by default) for files older than a certain number of days and for empty directories. It then presents its findings with a touch of apocalyptic whimsy and offers to 'sweep' them away (i.e., delete them). You can perform a dry run to see what would be swept or bypass confirmation for automated cleanups.

## Usage
```bash
./src/dust_bunny_sweeper.sh [OPTIONS]
```

### Options:
- `-d <directory>`: Specify the directory to scan. Defaults to the current directory (`.`).
- `-a <age_in_days>`: Set the age threshold in days. Files older than this will be considered dust bunnies. Defaults to `7` days.
- `-n`: Perform a dry run. The script will list what it *would* sweep but will not ask for confirmation or make any changes.
- `-y`: Assume 'yes' to all prompts. Use with extreme caution, as this will delete files and directories without asking for confirmation.
- `-h`: Display the help message and exit.

### Examples:
1. **Scan the current directory for files older than 7 days and empty directories (default behavior), then confirm deletion:**
   ```bash
   ./src/dust_bunny_sweeper.sh
   ```

2. **Scan a specific directory (`/var/log/old`) for files older than 30 days, with a dry run:**
   ```bash
   ./src/dust_bunny_sweeper.sh -d /var/log/old -a 30 -n
   ```

3. **Sweep away all dust bunnies in your home directory older than 14 days without confirmation (use with caution!):**
   ```bash
   ./src/dust_bunny_sweeper.sh -d ~/ -a 14 -y
   ```

## Installation
Simply clone the repository and navigate to the utility's directory. The script is self-contained.

```bash
# Assuming you are in the root of the ApocalypsAI repository
cd bash-utils/nightly-digital-dust-bunny-sweeper
chmod +x src/dust_bunny_sweeper.sh
```

## Contributing
Feel free to suggest new whimsical messages, improve the sweeping logic, or add more sophisticated filtering options!
