# nightly-quick-disk-usage-report

A lightweight Bash script that scans a directory and prints the *N* largest entries (files or sub‑directories) sorted by size.

## Features

- Works on any POSIX‑compatible system with `du`, `sort`, `head`, and `awk`.
- Choose the target directory (`-d`) and how many results to show (`-n`).
- Outputs size in bytes for easy scripting; pipe to `numfmt --to=iec` for human‑readable units.
- No external dependencies – just a single shell script.

## Installation

```bash
# Clone the repository (or copy the script) into your PATH
mkdir -p ~/bin && cp src/disk_report.sh ~/bin/quick-disk-report
chmod +x ~/bin/quick-disk-report
```

## Usage

```bash
# Show the top 10 largest entries in the current directory
quick-disk-report

# Show the top 5 largest entries in /var/log
quick-disk-report -d /var/log -n 5

# Human‑readable output (optional)
quick-disk-report | numfmt --to=iec
```

## Options

| Flag | Description |
|------|-------------|
| `-d <dir>` | Directory to scan (default: current directory). |
| `-n <num>` | Number of entries to display (default: 10). |
| `-h` | Show help and exit. |

## License

MIT © ApocalypsAI Community
