# nightly-arcane-archive-assistant

A whimsical Bash utility that helps you locate and optionally archive oversized files in a directory, presenting them with mystical messages. Useful for cleaning up disk space on servers or personal machines.

## Usage

```sh
./arcane-archive.sh [options] <directory>
```

**Options**
- `-t <size>` : size threshold (e.g., 10M, 500K). Default: 10M.
- `-m`       : actually move files to an `archive/` subdirectory (dry‑run by default).
- `-h`       : show help.

The script will list files larger than the threshold, prefixing each with a magical phrase. With `-m`, it moves them into `archive/` preserving directory structure.

## Example

```sh
./arcane-archive.sh -t 5M -m /var/log
```

## License

MIT
