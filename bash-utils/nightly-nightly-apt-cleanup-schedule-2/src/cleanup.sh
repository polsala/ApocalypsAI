#!/usr/bin/env bash

set -e

# Default options
dry_run=false
install_cron=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      dry_run=true
      shift
      ;;
    --install-cron)
      install_cron=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Function that performs the apt autoremove (or dry‑run)
list_removable() {
  if $dry_run; then
    apt-get autoremove --dry-run -y
  else
    apt-get autoremove -y
  fi
}

# Execute the removal (or dry‑run)
list_removable

# If requested, install a daily cron job that runs in dry‑run mode
if $install_cron; then
  # Resolve the absolute path of this script
  script_path=$(realpath "$0")
  cron_line="0 3 * * * $script_path --dry-run"
  # Preserve existing crontab entries, add the new one, and install
  (crontab -l 2>/dev/null || true; echo "$cron_line") | crontab -
  echo "Cron job installed to run daily at 3 AM (dry‑run)."
fi
