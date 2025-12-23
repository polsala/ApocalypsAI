Nightly Disk Usage Summary

This utility prints the top N largest directories under a specified path, with sizes in human‑readable format. It is useful for quickly spotting disk space hogs.

Usage:
  nightly-disk-usage-summary [path] [N]

Examples:
  nightly-disk-usage-summary /var/log 5
  nightly-disk-usage-summary . 10

If no path is given, the current directory is used. If N is omitted, 10 is used.
