#!/usr/bin/env bash
set -euo pipefail

# Default values
DIR="."
TOP=5
ARCHIVE_DAYS=""

print_help() {
  cat <<'EOF'
Usage: disk-space-guardian.sh [-d DIRECTORY] [-n COUNT] [-a DAYS]

  -d DIRECTORY   Directory to scan (default: current directory)
  -n COUNT       Number of top entries to display (default: 5)
  -a DAYS        Archive files older than DAYS into a tar.gz archive
EOF
}

# Parse arguments
while getopts ":d:n:a:h" opt; do
  case $opt in
    d) DIR="$OPTARG" ;;
    n) TOP="$OPTARG" ;;
    a) ARCHIVE_DAYS="$OPTARG" ;;
    h) print_help; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; print_help; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; print_help; exit 1 ;;
  esac
done

if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory '$DIR' does not exist." >&2
  exit 1
fi

echo -e "\e[1;34mScanning directory: $DIR\e[0m"
echo -e "\e[1;33mTop $TOP biggest files/directories:\e[0m"
du -ah "$DIR" 2>/dev/null | sort -rh | head -n "$TOP"

if [[ -n "$ARCHIVE_DAYS" ]]; then
  ARCHIVE_NAME="archive-$(date +%F).tar.gz"
  echo -e "\e[1;32mArchiving files older than $ARCHIVE_DAYS days into $ARCHIVE_NAME\e[0m"
  # Find files older than ARCHIVE_DAYS days
  mapfile -t OLD_FILES < <(find "$DIR" -type f -mtime +"$ARCHIVE_DAYS" -print)
  if [[ ${#OLD_FILES[@]} -eq 0 ]]; then
    echo "No files older than $ARCHIVE_DAYS days found."
  else
    tar -czf "$ARCHIVE_NAME" "${OLD_FILES[@]}"
    echo "Archived ${#OLD_FILES[@]} files."
  fi
fi
