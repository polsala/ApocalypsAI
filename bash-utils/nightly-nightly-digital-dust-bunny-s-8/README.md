# Nightly Digital Dust Bunny Sweeper

A whimsical yet practical bash utility to help keep your digital spaces tidy by sweeping away old, forgotten files – your "digital dust bunnies." This script identifies and optionally removes files older than a specified number of days from designated directories.

## Features

- **Configurable Directories**: Specify multiple paths to clean.
- **Age Threshold**: Define how old a file must be to be considered a "dust bunny."
- **Dry Run Mode**: See what files *would* be removed without actually deleting anything.
- **Logging**: Outputs actions to stdout, useful for cron jobs or automation.

## Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS] <DIRECTORY1> [DIRECTORY2...]
```

### Options

- `-a <DAYS>`, `--age <DAYS>`: Files older than `DAYS` will be considered for removal. Default is 7 days.
- `-d`, `--dry-run`: Perform a dry run. Files will be identified, but *not* deleted. This is the default behavior if no `-s` or `--sweep` is provided.
- `-s`, `--sweep`: Actually delete the identified files. **Use with caution!**
- `-h`, `--help`: Display this help message.

### Examples

1. **Dry run to see files older than 30 days in `/tmp` and `/var/log`**:
   ```bash
   ./src/dust_bunny_sweeper.sh -a 30 -d /tmp /var/log
   ```

2. **Actually sweep files older than 7 days in `/var/cache`**:
   ```bash
   ./src/dust_bunny_sweeper.sh -s /var/cache
   ```

3. **Sweep files older than 1 day in a custom directory**:
   ```bash
   ./src/dust_bunny_sweeper.sh -a 1 -s ~/my_temp_files
   ```

## Configuration

The script can also be configured using environment variables:

- `DUST_BUNNY_AGE_DAYS`: Overrides the default age threshold (e.g., `DUST_BUNNY_AGE_DAYS=14`).
- `DUST_BUNNY_DRY_RUN`: Set to `true` or `1` to enable dry run by default (e.g., `DUST_BUNNY_DRY_RUN=true`).
- `DUST_BUNNY_SWEEP`: Set to `true` or `1` to enable actual sweeping by default (e.g., `DUST_BUNNY_SWEEP=true`). Command-line `-s` takes precedence.

## Installation

Simply place the `src/dust_bunny_sweeper.sh` script in your desired location and make it executable:

```bash
chmod +x src/dust_bunny_sweeper.sh
```

## Safety Notice

Always perform a dry run (`-d` or no `-s` option) before executing a sweep (`-s`) to ensure you understand which files will be affected. The ApocalypsAI Nightly Integrator is not responsible for accidentally swept digital treasures!
