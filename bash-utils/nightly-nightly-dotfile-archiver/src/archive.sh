#!/usr/bin/env bash
set -euo pipefail

# Default max backups
MAX_BACKUPS="${MAX_BACKUPS:-5}"

usage() {
  echo "Usage: $0 <backup-dir> <file1> [file2 ...]" >&2
  exit 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

backup_dir="$1"
shift
files=("$@")

# Ensure backup directory exists
mkdir -p "$backup_dir"

timestamp=$(date +%Y%m%d-%H%M%S)
archive_name="backup-${timestamp}.tar.gz"
archive_path="${backup_dir}/${archive_name}"

# Create archive
tar -czf "$archive_path" "${files[@]}"

# Rotate old backups
if [[ -d "$backup_dir" ]]; then
  mapfile -t archives < <(ls -1t "${backup_dir}"/*.tar.gz 2>/dev/null || true)
  count=${#archives[@]}
  if (( count > MAX_BACKUPS )); then
    for (( i=MAX_BACKUPS; i<count; i++ )); do
      rm -f "${archives[i]}"
    done
  fi
fi

echo "Created archive: $archive_path"
