#!/usr/bin/env bash
set -euo pipefail

print_usage() {
  cat <<'EOF'
Usage: $0 -d <directory> -t <threshold_mb> -r <trash_dir> [-a]
  -d   Directory to scan (required)
  -t   Size threshold in megabytes (required)
  -r   Trash directory where large files will be moved (required)
  -a   Automatically move the found files (optional)
EOF
  exit 1
}

# Default values
AUTO_MOVE=false

# Parse arguments
while getopts ":d:t:r:a" opt; do
  case $opt in
    d) SCAN_DIR="$OPTARG";;
    t) THRESHOLD_MB="$OPTARG";;
    r) TRASH_DIR="$OPTARG";;
    a) AUTO_MOVE=true;;
    \?) echo "Invalid option: -$OPTARG" >&2; print_usage;;
    :) echo "Option -$OPTARG requires an argument." >&2; print_usage;;
  esac
done

# Validate required arguments
if [[ -z "${SCAN_DIR:-}" || -z "${THRESHOLD_MB:-}" || -z "${TRASH_DIR:-}" ]]; then
  echo "Error: missing required arguments." >&2
  print_usage
fi

# Ensure scan directory exists
if [[ ! -d "$SCAN_DIR" ]]; then
  echo "Error: scan directory '$SCAN_DIR' does not exist." >&2
  exit 1
fi

# Find files larger than the threshold
mapfile -t LARGE_FILES < <(find "$SCAN_DIR" -type f -size "+${THRESHOLD_MB}M" 2>/dev/null)

if [[ ${#LARGE_FILES[@]} -eq 0 ]]; then
  echo "🪐 No files larger than ${THRESHOLD_MB} MiB found in $SCAN_DIR."
  exit 0
fi

echo "🚀 Found ${#LARGE_FILES[@]} file(s) larger than ${THRESHOLD_MB} MiB:"
for f in "${LARGE_FILES[@]}"; do
  echo "  - $f"
done

if $AUTO_MOVE; then
  # Create trash directory if it does not exist
  mkdir -p "$TRASH_DIR"
  echo "🗑️ Moving files to trash directory: $TRASH_DIR"
  for f in "${LARGE_FILES[@]}"; do
    mv "$f" "$TRASH_DIR/"
    echo "   moved: $(basename "$f")"
  done
  echo "✅ Move complete."
else
  echo "💡 Run with -a to automatically move these files to the trash directory."
fi
