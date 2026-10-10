#!/usr/bin/env bash
set -euo pipefail

# Create temporary workspace
workdir=$(mktemp -d)
backup_dir="${workdir}/backups"
mkdir -p "$backup_dir"

# Create dummy dotfiles
echo "bashrc content" > "${workdir}/.bashrc"
echo "vimrc content" > "${workdir}/.vimrc"

# Path to the script (relative to this test file)
script_path="$(dirname "$0")/../src/archive.sh"

# Run the archiver
bash "$script_path" "$backup_dir" "${workdir}/.bashrc" "${workdir}/.vimrc"

# Verify an archive was created
archive=$(ls "$backup_dir"/backup-*.tar.gz)
if [[ -z "$archive" ]]; then
  echo "FAIL: No archive created"
  exit 1
fi

# Extract to a new dir and compare contents
extract_dir="${workdir}/extracted"
mkdir -p "$extract_dir"

tar -xzf "$archive" -C "$extract_dir"

if ! diff -q "${workdir}/.bashrc" "$extract_dir/.bashrc" >/dev/null; then
  echo "FAIL: .bashrc content mismatch"
  exit 1
fi

if ! diff -q "${workdir}/.vimrc" "$extract_dir/.vimrc" >/dev/null; then
  echo "FAIL: .vimrc content mismatch"
  exit 1
fi

echo "PASS: Archive created and contents verified"
