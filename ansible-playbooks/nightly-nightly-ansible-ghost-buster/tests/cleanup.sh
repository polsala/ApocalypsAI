#!/usr/bin/env bash
# Mock rationale: tidy up the environment so repeated runs are idempotent
set -e
rm -rf "/tmp/ghost_test_dir" "/tmp/ghosts.tar.gz"
