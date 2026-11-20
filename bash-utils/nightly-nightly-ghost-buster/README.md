# nightly-ghost-buster

**nightly‑ghost‑buster** is a tiny Bash utility that hunts down *ghost files* – files that occupy no space (zero‑byte) – in a given directory.  It can run in a dry‑run mode to simply report how many ghosts were found, or it can delete them for you.

## Features

- Recursively scans a directory for zero‑byte regular files.
- Outputs a concise JSON summary (`directory`, `action`, `ghost_count`).
- Optional `--delete` flag to actually remove the ghosts.
- Safe defaults – dry‑run only, no files are removed unless you ask.

## Installation

Copy the script to a location in your `$PATH` or invoke it directly from the repository:

```bash
chmod +x src/ghost_buster.sh
```

## Usage

```bash
./src/ghost_buster.sh [-d DIRECTORY] [--delete]
```

- `-d DIRECTORY` – Directory to scan (default: current directory `.`).
- `--delete` – Actually delete the discovered zero‑byte files. Without this flag the utility only reports.
- `-h` or `--help` – Show help.

### Examples

```bash
# Dry‑run in the current folder
./src/ghost_buster.sh

# Scan /var/log without deleting
./src/ghost_buster.sh -d /var/log

# Find and delete ghosts in ~/tmp
./src/ghost_buster.sh -d ~/tmp --delete
```

Typical output (JSON on a single line):

```json
{"directory":"/home/user/tmp","action":"found","ghost_count":3}
```

When `--delete` is used the `action` field becomes `"deleted"`.

## Testing

Run the bundled test script:

```bash
cd tests && bash test_ghost_buster.sh
```

The test creates a temporary directory with a mix of empty and non‑empty files, verifies the dry‑run count, then runs the delete mode and confirms the empty files are removed.
