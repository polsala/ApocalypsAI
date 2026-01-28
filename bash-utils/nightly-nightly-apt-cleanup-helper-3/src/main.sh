#!/usr/bin/env bash
set -euo pipefail

# Function to invoke apt-get (real or mocked)
apt_get() {
  if [[ "${APT_MOCK:-}" == "1" ]]; then
    cat <<'EOF'
Reading package lists...
Building dependency tree...
Reading state information...
The following packages will be REMOVED:
  libfoo1 libbar2
0 upgraded, 0 newly installed, 2 to remove and 0 not upgraded.
After this operation, 5 MB of disk space will be freed.
EOF
  else
    command apt-get -s autoremove "$@"
  fi
}

usage() {
  echo "Usage: $0 [--dry-run|--clean]"
  exit 1
}

# Default mode is dry‑run
mode="dry"

while (( "$#" )); do
  case "$1" in
    --dry-run) mode="dry"; shift ;;
    --clean)   mode="clean"; shift ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ "$mode" == "dry" ]]; then
  echo "Packages that would be removed:"
  # Capture simulated apt-get output
  apt_output=$(apt_get)
  # Extract the line after the marker and split into individual package names
  packages=$(echo "$apt_output" | awk '/The following packages will be REMOVED:/ {getline; print}')
  for pkg in $packages; do
    echo "$pkg"
  done
else
  echo "Running apt-get autoremove..."
  apt-get autoremove -y
  echo "Cleaning apt cache..."
  apt-get clean
fi
