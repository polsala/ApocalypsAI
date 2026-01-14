Nightly Disk Usage Report

Overview: This utility scans a directory and prints a list of its immediate sub‑directories and files sorted by size in descending order, using human‑readable units.

Installation: Place the script somewhere in your PATH and make it executable.

Usage:
  nightly-disk-usage-report [options] [path]

Options:
  -h, --help        Show help and exit
  -d N, --depth N   Limit recursion depth to N (default: 1)

Examples:
  nightly-disk-usage-report /var/log
  nightly-disk-usage-report -d 2 .
