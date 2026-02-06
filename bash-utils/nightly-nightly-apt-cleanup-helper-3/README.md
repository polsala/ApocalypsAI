# Nightly Apt Cleanup Helper

## Overview

`nightly-apt-cleanup-helper` is a tiny Bash script that lets you peek into what your Debian/Ubuntu system *could* clean up with `apt-get autoremove` and `apt-get clean`.  By default it runs in **dry‑run** mode, printing the packages that would be removed and indicating that the cache would be cleaned.  Pass `--execute` to actually perform the operations (requires `sudo`).

The script is deliberately whimsical – it pretends to be a post‑apocalyptic “scavenger” that decides which packages are no longer needed for the wasteland.

## Installation

```bash
# Clone the repository (or copy the files) and make the script executable
chmod +x src/main.sh
# Optionally symlink it into your $PATH
sudo ln -s $(pwd)/src/main.sh /usr/local/bin/apt-cleanup
```

## Usage

```bash
# Dry‑run (default) – safe, no changes made
./src/main.sh

# Actually run the cleanup (will invoke sudo)
./src/main.sh --execute
```

### Options

- `--execute` Run the real `apt-get autoremove` and `apt-get clean` commands.
- No flag    Run in dry‑run mode (default).

## How it works

The script calls `apt-get -s autoremove` to simulate an autoremove and extracts the package names.  It also simulates a cache clean.  For testing purposes you can set the environment variable `MOCK_APT=1` to use built‑in mock data instead of invoking the real package manager.

## Testing

The utility ships with a small Bash test suite located in `tests/`.  Run it with:

```bash
cd tests && bash test_main.sh
```

All tests should pass on any Linux system without requiring root privileges.
