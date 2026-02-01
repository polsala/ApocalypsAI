#!/usr/bin/env bash
set -euo pipefail

# nightly-apt-cleanup-helper
# ------------------------------------------------------------
# Shows which packages would be auto‑removed and simulates cache cleaning.
# By default runs in dry‑run mode; use --execute to actually perform actions.
# ------------------------------------------------------------

# Mock rationale: When MOCK_APT=1 we replace real apt calls with static data
# so tests can run offline without root or network access.
if [[ "${MOCK_APT:-0}" == "1" ]]; then
  list_autoremove() {
    echo -e "libfoo\nlibbar"
  }
  list_cache() {
    echo "apt-get clean simulated"
  }
else
  list_autoremove() {
    # Simulate autoremove and extract package names
    apt-get -s autoremove 2>/dev/null | grep "^Remv" | awk '{print $2}'
  }
  list_cache() {
    # Some apt versions support -s for clean; fallback to a placeholder
    if apt-get clean -s >/dev/null 2>&1; then
      apt-get clean -s
    else
      echo "apt-get clean -s not supported on this system"
    fi
  }
fi

# Parse arguments
DRY_RUN=true
if [[ "${1:-}" == "--execute" ]]; then
  DRY_RUN=false
  shift
fi

if $DRY_RUN; then
  echo "Packages that would be auto-removed:"
  list_autoremove
  echo "Would clean apt cache."
else
  echo "Running autoremove..."
  sudo apt-get -y autoremove
  echo "Cleaning apt cache..."
  sudo apt-get clean
fi
