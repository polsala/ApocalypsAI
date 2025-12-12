#!/bin/bash
# Mock rationale: This script orchestrates the entire test suite, ensuring a clean setup,
# execution of the main playbook in different modes, and verification of outcomes.

set -euo pipefail

echo "--- Running Digital Dust Bunny Sweeper Tests ---"

# Define paths
TEST_DIR="/tmp/digital_dust_bunnies_test"
REPORT_PATH="/tmp/dust_bunny_sweeper_report_localhost.txt"
INVENTORY_FILE="inventory_test.ini"
MAIN_PLAYBOOK="../dust_bunny_sweeper.yml"
VERIFY_DRY_RUN_PLAYBOOK="verify_dry_run.yml"
VERIFY_CLEANUP_PLAYBOOK="verify_cleanup.yml"

# Change to the tests directory to ensure relative paths work
cd "$(dirname "$0")"

# 1. Setup mock files
echo "1. Setting up mock files..."
./mock_files_setup.sh

# 2. Run main playbook in dry-run mode
echo "2. Running main playbook in DRY RUN mode..."
ansible-playbook -i "$INVENTORY_FILE" "$MAIN_PLAYBOOK" \
  -e "dry_run=true scan_paths=['$TEST_DIR'] file_age_days=7 report_path=$REPORT_PATH"

# 3. Verify dry-run results
echo "3. Verifying DRY RUN results..."
ansible-playbook -i "$INVENTORY_FILE" "$VERIFY_DRY_RUN_PLAYBOOK"

# 4. Run main playbook in actual cleanup mode
echo "4. Running main playbook in ACTUAL CLEANUP mode..."
ansible-playbook -i "$INVENTORY_FILE" "$MAIN_PLAYBOOK" \
  -e "dry_run=false scan_paths=['$TEST_DIR'] file_age_days=7 report_path=$REPORT_PATH"

# 5. Verify cleanup results
echo "5. Verifying CLEANUP results..."
ansible-playbook -i "$INVENTORY_FILE" "$VERIFY_CLEANUP_PLAYBOOK"

# 6. Cleanup mock files
echo "6. Cleaning up mock files..."
./mock_files_cleanup.sh

echo "--- All Digital Dust Bunny Sweeper tests passed! ---"
