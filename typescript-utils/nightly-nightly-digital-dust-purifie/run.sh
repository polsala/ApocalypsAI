#!/bin/bash
set -euo pipefail

# This script builds and runs the Nightly Digital Dust Purifier.

# Ensure node_modules are installed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

echo "Building TypeScript project..."
npm run build

echo "Running Nightly Digital Dust Purifier (dry-run example):"
echo "  Scanning current directory for files older than 90 days, excluding node_modules and .git."
echo "  (No files will be moved or deleted in dry-run mode.)"
node dist/index.js . --age 90 --dry-run

echo "\nTo run with actual archiving (use with caution!):"
echo "  node dist/index.js . --age 180 --archive-dir ./dust_bunnies_archive"
echo "\nTo run tests:"
echo "  npm test"
