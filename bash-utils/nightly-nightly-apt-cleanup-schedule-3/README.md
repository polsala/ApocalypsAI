# nightly-apt-cleanup-scheduler

Utility that helps you keep your Debian/Ubuntu system tidy by cleaning the apt cache. It can be run manually or installed as a daily cron job. While it works, it sprinkles apocalypse‑themed warnings to keep the terminal entertaining.

## Usage

```bash
./nightly-apt-cleanup-scheduler.sh [--dry-run] [--install-cron] [--remove-cron]
```

- `--dry-run` : show what would be removed without actually deleting.
- `--install-cron` : install a daily cron entry at 02:42 AM.
- `--remove-cron` : remove the installed cron entry.

## How it works

1. Lists packages in `/var/cache/apt/archives` older than 7 days.
2. Optionally removes them with `sudo apt-get clean`.
3. Prints a random apocalypse quote before and after the operation.

## Uninstall cron

Run with `--remove-cron` to delete the installed cron entry.

## License

MIT
