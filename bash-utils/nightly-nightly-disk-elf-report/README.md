# nightly-disk-elf-report

Generates a whimsical, emoji‑filled report of the largest files in a directory.

## Usage

```sh
./src/disk-elf-report.sh [directory] [count]
```

- `directory` – path to scan (default: current directory)
- `count` – number of top files to show (default: 10)

The report lists size, path, and an emoji representing the file’s magnitude.

## Example

```sh
$ ./src/disk-elf-report.sh /var/log 5
🧚  12K  /var/log/syslog
🐉  3.4M /var/log/kern.log
🦖  27M  /var/log/mysql/error.log
🐢  150M /var/log/backup.tar.gz
```

## How it works

The script uses `du -b` (via `find -printf`) to get file sizes in bytes, sorts them, picks the top N, then maps size ranges to emojis:
- < 1 MiB → 🧚 (fairy)
- < 10 MiB → 🐉 (dragon)
- < 100 MiB → 🦖 (dinosaur)
- ≥ 100 MiB → 🐢 (turtle)

It prints a human‑readable size using `numfmt`.
