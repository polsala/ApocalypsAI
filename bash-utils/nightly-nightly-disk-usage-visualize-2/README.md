# nightly-disk-usage-visualizer

A whimsical Bash utility that visualizes disk usage of a directory as a sorted tree, helping you spot space hogs in a post‑apocalyptic file system.

## Usage

```sh
./disk-usage.sh [options] <directory>
```

**Options**
- `-d <depth>`: maximum depth to display (default: 2)
- `-h`: human‑readable sizes (default)

**Example**

```sh
./disk-usage.sh -d 3 /var/log
```

The script prints a list of directories/files with their sizes, sorted from largest to smallest.
