# nightly-disk-space-guardian

Utility to scan a directory for files larger than a given size and optionally move them to a trash folder. Helps keep disk usage tidy in a whimsical post‑apocalyptic style.

## Usage

```sh
./src/main.sh -d /path/to/scan -t 100 -r /path/to/trash [-a]
```

- `-d` directory to scan (required)
- `-t` size threshold in megabytes (required)
- `-r` trash directory where large files will be moved (required)
- `-a` automatically move the found files; without it the script only reports.

The script prints colorful messages and a summary.

## Example

```sh
./src/main.sh -d /var/log -t 50 -r ~/trash -a
```

Will move all log files larger than 50 MiB to `~/trash`.

## License

MIT
