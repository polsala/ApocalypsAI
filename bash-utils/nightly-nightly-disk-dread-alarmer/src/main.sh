#!/usr/bin/env bash
set -euo pipefail

# Default threshold: 100 MiB (in KiB)
DEFAULT_THRESHOLD_KB=102400

usage() {
  echo "Usage: $0 <directory> [threshold_kb]"
}

# Retrieve the size of a directory in KiB using du
get_dir_size_kb() {
  local dir="$1"
  du -sk "$dir" | cut -f1
}

# Core check function – prints a whimsical message based on size
# Arguments:
#   $1 – directory name (for messaging)
#   $2 – size in KiB
#   $3 – optional threshold in KiB (defaults to DEFAULT_THRESHOLD_KB)
check_size() {
  local dir_name="$1"
  local size_kb="$2"
  local threshold_kb="${3:-$DEFAULT_THRESHOLD_KB}"

  if (( size_kb > threshold_kb )); then
    # Use numfmt for human‑readable output; fallback to raw value if unavailable
    local human=$(numfmt --to=iec "${size_kb}K" 2>/dev/null || echo "${size_kb}K")
    echo "⚠️  The abyss of $dir_name grows to $human!"
    return 1
  else
    echo "✅  $dir_name is within safe limits."
    return 0
  fi
}

# Entry point when script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi

  dir_path="$1"
  threshold_kb="${2:-$DEFAULT_THRESHOLD_KB}"

  size_kb=$(get_dir_size_kb "$dir_path")
  check_size "$dir_path" "$size_kb" "$threshold_kb"
fi
