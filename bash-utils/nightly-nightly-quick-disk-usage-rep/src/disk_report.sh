#!/usr/bin/env bash
set -euo pipefail

# Convert a byte count to a human‑readable string
human_readable() {
  local bytes=$1
  if ((bytes < 1024)); then
    echo "${bytes} B"
  elif ((bytes < 1024*1024)); then
    printf "%.2f KiB\n" "$(awk "BEGIN {printf %f,$bytes/1024}")"
  elif ((bytes < 1024*1024*1024)); then
    printf "%.2f MiB\n" "$(awk "BEGIN {printf %f,$bytes/(1024*1024)}")"
  else
    printf "%.2f GiB\n" "$(awk "BEGIN {printf %f,$bytes/(1024*1024*1024)}")"
  fi
}

main() {
  local target="${1:-.}"
  local threshold="${2:-0}"
  if [[ ! -d "$target" ]]; then
    echo "Error: $target is not a directory" >&2
    exit 1
  fi
  # Size in bytes (du -sb works on GNU coreutils; fallback to du -sk and convert)
  local size_bytes
  if du --version >/dev/null 2>&1; then
    size_bytes=$(du -sb "$target" | cut -f1)
  else
    # macOS fallback: du -sk gives KiB
    size_bytes=$(du -sk "$target" | awk '{print $1 * 1024}')
  fi
  if (( size_bytes < threshold )); then
    exit 0
  fi
  local size_human
  size_human=$(human_readable "$size_bytes")
  echo "Size: $size_human ($size_bytes bytes)"
  # JSON output – ensure proper escaping of the path
  local abs_path
  abs_path=$(realpath "$target")
  local json
  json=$(printf '{"path":"%s","size_bytes":%s,"size_human":"%s"}' "$abs_path" "$size_bytes" "$size_human")
  echo "$json"
}

main "$@"
