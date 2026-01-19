#!/usr/bin/env bash

set -euo pipefail

DIR="${1:-$HOME/.ssh}"

if [[ ! -d "$DIR" ]]; then
  echo "Directory $DIR does not exist."
  exit 1
fi

echo "Scanning SSH keys in $DIR..."

found_issue=0

while IFS= read -r -d '' keyfile; do
  # Skip public key files
  if [[ "$keyfile" == *.pub ]]; then
    continue
  fi

  perms=$(stat -c %a "$keyfile")
  if [[ "$perms" -ne 600 ]]; then
    echo "⚠️  Permissions for $keyfile are $perms, should be 600"
    found_issue=1
  fi

  # Get key info via ssh-keygen
  if output=$(ssh-keygen -lf "$keyfile" 2>/dev/null); then
    bits=$(echo "$output" | awk '{print $1}')
    type=$(echo "$output" | awk -F'[()]' '{print $2}')
    echo "🔑 $keyfile: $bits bits $type"
    if [[ "$type" == "RSA" && "$bits" -lt 2048 ]]; then
      echo "⚠️  RSA key $keyfile is weaker than 2048 bits"
      found_issue=1
    fi
  else
    echo "⚠️  Unable to read $keyfile with ssh-keygen"
    found_issue=1
  fi
done < <(find "$DIR" -type f -print0)

if [[ $found_issue -eq 0 ]]; then
  echo "✅ All SSH keys look good!"
fi
