# nightly-dustbuster

A whimsical bash utility that hunts down forgotten temporary, cache, and log files, reports their total size, and can clean them up for you.

## Features
- Scan a directory (default current) for common junk patterns (`*.tmp`, `*.log`, `__pycache__`, `.cache`, `node_modules`).
- Show total size of found junk.
- Dry‑run mode to preview what would be removed.
- Optional clean mode to delete after a safety prompt.

## Installation
```sh
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/bash-utils/nightly-dustbuster
chmod +x src/dustbuster.sh
```

## Usage
```sh
./src/dustbuster.sh [-d DIR] [-r] [-c]
  -d DIR   Directory to scan (default: .)
  -r       Dry‑run (default). Only list files.
  -c       Clean mode. Prompt before deleting.
```

## Example
```sh
# Preview junk in the home directory
./src/dustbuster.sh -d $HOME

# Actually delete after confirmation
./src/dustbuster.sh -d $HOME -c
```

## License
MIT
