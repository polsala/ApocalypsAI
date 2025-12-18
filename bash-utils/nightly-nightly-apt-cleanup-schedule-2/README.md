# nightly‑apt‑cleanup‑scheduler

**Purpose**: A whimsical yet practical Bash utility that helps keep your Debian/Ubuntu system tidy by running `apt-get autoremove`. It supports a dry‑run mode for safety and can install a daily cron job that performs a dry‑run cleanup at 3 AM.

## Usage
```bash
./cleanup.sh [--dry-run] [--install-cron]
```

- `--dry-run` – Show what would be removed without actually uninstalling anything. This is the default when the flag is supplied.
- `--install-cron` – Adds a cron entry that runs the script every day at 3 AM in dry‑run mode. Useful for getting regular reports of unused packages.

## Examples
```bash
# See what would be removed (no changes made)
./cleanup.sh --dry-run

# Actually remove the packages
./cleanup.sh

# Install a daily dry‑run cron job
./cleanup.sh --install-cron
```

## Safety notes
- The script only calls `apt-get autoremove`. It never runs `apt-get upgrade` or any other potentially disruptive command.
- When run without `--dry-run`, it passes `-y` to automatically confirm the removal. Review the output of a dry‑run first if you are cautious.

## Testing
Run the bundled test script:
```bash
bash tests/test_cleanup.sh
```
The test replaces `apt-get` with a mock that records invocations, ensuring the script behaves correctly without touching the real package manager.
