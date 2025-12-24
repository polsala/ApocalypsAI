#!/usr/bin/env bash
# nightly-apt-autoremove-helper
# ------------------------------------------------------------
# This script reports (and optionally applies) the packages that
# would be removed by `apt-get autoremove`.
# ------------------------------------------------------------

set -euo pipefail

# Default mode is dry‑run
DRY_RUN=true
APPLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --apply)
      APPLY=true
      DRY_RUN=false
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Function to invoke apt-get (allows test mocking via PATH)
apt_get() {
  command apt-get "$@"
}

# Run a simulated autoremove to capture the list of packages
simulate_output=$(apt_get -s autoremove)

# Parse package names from the simulated output
packages=()
capture=false
while IFS= read -r line; do
  if $capture; then
    # Stop when we hit an empty line
    [[ -z "$line" ]] && break
    # Trim leading whitespace and add to list
    pkg=$(echo "$line" | sed -E 's/^\s+//')
    packages+=("$pkg")
  elif [[ "$line" == "The following packages will be REMOVED:"* ]]; then
    capture=true
  fi
done <<< "$simulate_output"

if [[ ${#packages[@]} -eq 0 ]]; then
  echo "No packages to remove."
  exit 0
fi

# Output the dry‑run summary
echo "Packages that would be removed:"
for pkg in "${packages[@]}"; do
  echo "  $pkg"
done

# If --apply was requested, perform the actual removal
if $APPLY; then
  echo "Proceeding with apt-get autoremove -y ..."
  apt_get autoremove -y
fi
