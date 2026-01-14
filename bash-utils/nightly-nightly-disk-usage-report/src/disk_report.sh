#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: $(basename "$0") [options] [path]

Options:
  -h, --help        Show this help message and exit
  -d N, --depth N   Limit recursion depth to N (default: 1)

If no path is supplied, the current directory is used.
EOF
}

# Default values
path="."
depth=1

# Parse options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    -d|--depth)
      if [[ -n "${2-}" && "${2}" != -* ]]; then
        depth="$2"
        shift
      else
        echo "Error: --depth requires a numeric argument" >&2
        exit 1
      fi
      ;;
    *)
      if [[ -z "$path_set" ]]; then
        path="$1"
        path_set=1
      else
        echo "Error: Unexpected argument '$1'" >&2
        usage
        exit 1
      fi
      ;;
  esac
  shift
done

# Verify that the path exists and is a directory
if [[ ! -d "$path" ]]; then
  echo "Error: Path '$path' is not a directory" >&2
  exit 1
fi

# Generate report
# du -h prints human‑readable sizes, --max-depth limits recursion
# sort -hr sorts by human‑readable size descending

du -h --max-depth="$depth" "$path" 2>/dev/null | sort -hr
