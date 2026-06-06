#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [-d DIR] [-n]"
  echo "  -d DIR   SSH directory (default /etc/ssh)"
  echo "  -n       Dry run (no changes)"
  exit 1
}

# Default values
DIR="/etc/ssh"
DRY_RUN=0

while getopts ":d:n" opt; do
  case $opt in
    d) DIR="$OPTARG" ;;
    n) DRY_RUN=1 ;;
    *) usage ;;
  esac
done

if [[ ! -d "$DIR" ]]; then
  echo "Error: directory $DIR does not exist"
  exit 1
fi

timestamp=$(date +%s)

rotate_key() {
  local type=$1
  local file="${DIR}/ssh_host_${type}_key"
  if [[ -f "$file" ]]; then
    local backup="${file}.bak.${timestamp}"
    if (( DRY_RUN )); then
      echo "Would backup $file to $backup"
    else
      mv "$file" "$backup"
      echo "Backed up $file to $backup"
    fi
  fi
  if (( DRY_RUN )); then
    echo "Would generate $type key at $file"
  else
    ssh-keygen -q -t "$type" -b 4096 -f "$file" -N "" -C "rotated-$(date +%F)"
    echo "Generated $type key at $file"
  fi
}

for keytype in rsa ecdsa ed25519; do
  rotate_key "$keytype"
done

echo "SSH host key rotation complete."
