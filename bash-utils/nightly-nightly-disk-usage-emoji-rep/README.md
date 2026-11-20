# nightly-disk-usage-emoji-report

Utility that shows disk usage of a given directory with an emoji indicator:
- 🟢 low usage (<10%)
- 🟡 moderate usage (10‑50%)
- 🔴 high usage (>50%)

## Usage

```sh
./report.sh [path]
```

If no path is given, the current directory is used.

The script calculates the percentage of used space on the filesystem containing the path and prints the size together with the appropriate emoji.

## Example

```sh
$ ./report.sh /var
🟡 12G /var
```
