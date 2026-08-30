# nightly-disk-usage-report

## Summary
Generates a concise report of the largest files and directories in a given path.

## Usage
```sh
./src/disk_report.sh [directory] [count]
```
- `directory` (optional): Path to scan. Defaults to the current directory.
- `count` (optional): Number of top entries to display. Defaults to `10`.

The script prints a table with size (human‑readable) and path, sorted descending.

## Example
```sh
$ ./src/disk_report.sh /var/log 5
Size	Path
2.3M	/var/log/syslog
1.8M	/var/log/kern.log
...```

## Notes
- Requires standard Unix utilities (`du`, `sort`, `head`).
- Works on Linux and macOS (uses `du -b` on Linux, falls back to `du -k` on macOS).
