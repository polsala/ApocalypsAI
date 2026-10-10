# nightly-disk-space-guardian

A whimsical Bash utility that scans a directory, reports the largest consumers of disk space, and can archive old large files to keep your system tidy.

## Features

- Show top N biggest files/directories.
- Optionally archive files older than a given number of days into a tar.gz.
- Colorful output for readability.

## Usage

```sh
./disk-space-guardian.sh [-d DIRECTORY] [-n COUNT] [-a DAYS]
```

- `-d DIRECTORY` – directory to scan (default: current directory)
- `-n COUNT` – number of top entries to display (default: 5)
- `-a DAYS` – if set, archive files older than DAYS into `archive-$(date +%F).tar.gz`

## Examples

```sh
# Show top 10 biggest items in /var
./disk-space-guardian.sh -d /var -n 10

# Archive files older than 30 days in /home/user/downloads
./disk-space-guardian.sh -d /home/user/downloads -a 30
```

## License

MIT
