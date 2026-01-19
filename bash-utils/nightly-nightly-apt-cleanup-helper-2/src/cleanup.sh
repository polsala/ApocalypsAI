#!/usr/bin/env bash
set -euo pipefail

# Parse options
DRY_RUN=1
if [[ "${1:-}" == "-n" ]]; then
  DRY_RUN=1
  shift
else
  DRY_RUN=0
fi

DATA_DIR="${1:-}"
if [[ -z "$DATA_DIR" ]]; then
  echo "Usage: $0 [-n] <data-dir>"
  exit 1
fi

INSTALLED_FILE="$DATA_DIR/installed.txt"
AUTO_FILE="$DATA_DIR/auto_remove.txt"

if [[ ! -f "$INSTALLED_FILE" || ! -f "$AUTO_FILE" ]]; then
  echo "Missing required files in $DATA_DIR"
  exit 1
fi

# Read packages
mapfile -t installed < "$INSTALLED_FILE"
mapfile -t auto_remove < "$AUTO_FILE"

# Determine packages to purge
to_purge=()
for pkg in "${auto_remove[@]}"; do
  for i in "${installed[@]}"; do
    if [[ "$i" == "$pkg" ]]; then
      to_purge+=("$pkg")
    fi
  done
done

# Report
echo "=== Post‑Apocalypse APT Cleanup Report ==="
echo "Total installed packages: ${#installed[@]}"
echo "Auto‑removable packages detected: ${#auto_remove[@]}"
echo "Packages slated for removal: ${#to_purge[@]}"
if (( ${#to_purge[@]} > 0 )); then
  printf "  %s\n" "${to_purge[@]}"
else
  echo "  None. Your system is already lean."
fi

if (( DRY_RUN )); then
  echo "[Dry‑run] No changes made."
else
  # Simulate removal by filtering installed.txt
  grep -vxF -f <(printf "%s\n" "${to_purge[@]}") "$INSTALLED_FILE" > "$INSTALLED_FILE.tmp"
  mv "$INSTALLED_FILE.tmp" "$INSTALLED_FILE"
  echo "Removal simulated. Updated installed.txt."
fi
