#!/usr/bin/env bash
# Mock rationale: set up a deterministic environment with known ghost files
set -e
TEST_DIR="/tmp/ghost_test_dir"
ARCHIVE="/tmp/ghosts.tar.gz"

# Clean any leftovers from previous runs
rm -rf "${TEST_DIR}" "${ARCHIVE}"
mkdir -p "${TEST_DIR}"
# Create two dummy ghost files
echo "boo" > "${TEST_DIR}/spooky1.ghost"
echo "eek" > "${TEST_DIR}/spooky2.ghost"
# Also create a non‑ghost file to ensure it is ignored
echo "not a ghost" > "${TEST_DIR}/normal.txt"
