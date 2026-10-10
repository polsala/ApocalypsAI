# nightly-dotfile-archiver

A whimsical Bash utility that creates timestamped tar.gz archives of your dotfiles (or any files) and keeps only the most recent N backups.

## Features
- Simple command line: `archive.sh <backup-dir> <file1> [file2 ...]`
- Generates archive name `backup-YYYYmmdd-HHMMSS.tar.gz`
- Automatic rotation: keeps the latest `$MAX_BACKUPS` archives (default 5)
- Works with any files, not just dotfiles

## Installation
Copy `src/archive.sh` to a directory in your `$PATH` and make it executable.

## Usage
```sh
# Archive your .bashrc and .vimrc into ~/dotbackups
archive.sh ~/dotbackups ~/.bashrc ~/.vimrc
```

## Environment
- `MAX_BACKUPS` (optional) – maximum number of archives to retain. Older archives are deleted.

## License
MIT
