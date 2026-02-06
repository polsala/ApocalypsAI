#!/usr/bin/env bash
set -euo pipefail

# Default to dry‑run; -y performs actual deletions
DRY_RUN=true
while getopts ":y" opt; do
  case $opt in
    y) DRY_RUN=false ;;
    *) echo "Usage: $0 [-y]" >&2; exit 1 ;;
  esac
done

# Allow overriding the cache directory for testing
CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"
if [[ ! -d "$CACHE_DIR" ]]; then
  echo "Cache directory $CACHE_DIR not found." >&2
  exit 1
fi

declare -A latest_file

shopt -s nullglob
for file in "$CACHE_DIR"/*.deb; do
  basename=$(basename "$file")
  # Expected pattern: name_version_arch.deb
  IFS='_' read -r pkg ver archdeb <<< "$basename"
  # Remove any trailing underscores from version part (e.g., "1.0_amd64.deb")
  ver=${ver%_*}
  if [[ -z "${latest_file[$pkg]+x}" ]]; then
    latest_file[$pkg]="$file"
  else
    stored=$(basename "${latest_file[$pkg]}")
    IFS='_' read -r _ stored_ver _ <<< "$stored"
    stored_ver=${stored_ver%_*}
    if dpkg --compare-versions "$ver" "gt" "$stored_ver"; then
      latest_file[$pkg]="$file"
    fi
  fi
done

# Delete (or list) older files
for file in "$CACHE_DIR"/*.deb; do
  pkg=$(basename "$file" | cut -d'_' -f1)
  if [[ "${latest_file[$pkg]}" != "$file" ]]; then
    if $DRY_RUN; then
      echo "Would delete: $file"
    else
      echo "Deleting: $file"
      rm -f "$file"
    fi
  fi
done
