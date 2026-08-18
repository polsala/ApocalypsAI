#!/usr/bin/env bash
set -euo pipefail

# Configurable usage threshold (percentage). Default: 80%
THRESHOLD="${THRESHOLD:-80}"

# Retrieve df output; allow mocking via DF_OUTPUT for tests
get_df_output() {
  if [[ -n "${DF_OUTPUT:-}" ]]; then
    echo "$DF_OUTPUT"
  else
    df -hP
  fi
}

# Process each line of df output
while IFS= read -r line; do
  # Skip header line
  if [[ "$line" == Filesystem* ]]; then
    continue
  fi
  # Expected POSIX format: Filesystem Size Used Avail Use% Mounted on
  usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
  mount=$(echo "$line" | awk '{print $6}')
  filesystem=$(echo "$line" | awk '{print $1}')
  if (( usage > THRESHOLD )); then
    echo "⚠️ $filesystem mounted on $mount is ${usage}% full! Consider cleaning up."
  fi
done < <(get_df_output)
