#!/usr/bin/env bash
set -euo pipefail

# Function to list cached .deb files older than N days (default 30)
list_old_debs() {
  local days="${1:-30}"
  find /var/cache/apt/archives -type f -name "*.deb" -mtime +"$days" -print
}

# Function to remove given files
remove_files() {
  local files=("$@")
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "No old packages to remove."
    return
  fi
  sudo rm -f "${files[@]}"
  echo "Removed ${#files[@]} old package(s)."
}

# Main execution block
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  DAYS="${1:-30}"
  mapfile -t OLD_DEBS < <(list_old_debs "$DAYS")
  remove_files "${OLD_DEBS[@]}"
  # whimsical apocalypse message
  APoc_MESSAGES=(
    "The caches crumble, but hope remains."
    "Dust settles on the old packages."
    "Even the apt cache knows the end is near."
    "Cleaned! The apocalypse can wait."
  )
  RAND_IDX=$((RANDOM % ${#APoc_MESSAGES[@]}))
  echo "${APoc_MESSAGES[$RAND_IDX]}"
fi
