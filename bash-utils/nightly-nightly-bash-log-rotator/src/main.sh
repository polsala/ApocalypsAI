#!/usr/bin/env bash
set -euo pipefail

# Default parameters
DIR="."
AGE=7
RETENTION=30
DRY_RUN=0

# Parse options
while getopts "d:a:r:n" opt; do
  case $opt in
    d) DIR="$OPTARG" ;;
    a) AGE="$OPTARG" ;;
    r) RETENTION="$OPTARG" ;;
    n) DRY_RUN=1 ;;
    *) echo "Invalid option"; exit 1 ;;
  esac
done

log() {
  echo "[log-rotator] $*"
}

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] $*"
  else
    eval "$@"
  fi
}

# Compress old files (excluding already compressed ones)
log "Compressing files older than $AGE days in $DIR"
run "find \"$DIR\" -type f -mtime +$AGE ! -name \"*.gz\" -print -exec gzip {} \\;"

# Delete compressed files older than retention period
log "Deleting compressed files older than $RETENTION days in $DIR"
run "find \"$DIR\" -type f -name \"*.gz\" -mtime +$RETENTION -print -delete"

log "Done."
