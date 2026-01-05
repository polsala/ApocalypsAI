# nightly-apt-cleanup-scheduler

A tiny Bash utility that helps keep your Debian/Ubuntu system tidy by removing stale ``.deb`` files from the apt cache.  It can also install a daily cron job that prints a fun, apocalypse‑themed reminder each time it runs.

## Features

- **Dry‑run mode** – see what would be deleted without touching anything.
- **Configurable age** – specify how many days old a package must be before it is considered stale (default: 7 days).
- **One‑click cron installation** – creates a system‑wide cron entry that runs the cleanup every day at 02:00 AM (requires root).
- **Apocalypse‑themed messages** – each run prints a random “doomsday” quote to keep things entertaining.

## Installation

```sh
# Clone the repository (or copy the files into your own project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/bash-utils/nightly-apt-cleanup-scheduler
```

Make the script executable:

```sh
chmod +x src/cleanup.sh
```

## Usage

```sh
./src/cleanup.sh [options]
```

### Options

- `--dry-run`              Show which files would be removed, but do not delete them.
- `--max-age-days N`      Consider files older than *N* days as stale (default: `7`).
- `--install-cron`        Create a system‑wide cron job that runs this script daily at 02:00 AM.  Requires root privileges.

### Environment Variables

- `APT_CACHE_DIR` – Override the default apt cache directory (`/var/cache/apt/archives`).  Useful for testing.

## Example

```sh
# Dry‑run, showing files older than 5 days
export APT_CACHE_DIR="/tmp/fake-apt-cache"
./src/cleanup.sh --dry-run --max-age-days 5

# Actually delete stale files
./src/cleanup.sh --max-age-days 10

# Install the daily cron job (run as root)
sudo ./src/cleanup.sh --install-cron
```

## Testing

Run the bundled tests with Bash:

```sh
bash tests/test_cleanup.sh
```

The tests create a temporary fake apt cache, populate it with files of various ages, and verify that the script behaves correctly in both dry‑run and real‑run modes.
