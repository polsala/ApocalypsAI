#!/bin/bash

# Test suite for Nightly Digital Debris Scavenger

SCRIPT_PATH="../src/scavenge.sh"
TEST_DIR=""

# Setup function
setup() {
    TEST_DIR=$(mktemp -d)
    mkdir -p "${TEST_DIR}/subdir"
    echo "Test setup: Created ${TEST_DIR}"
}

# Teardown function
teardown() {
    if [[ -d "${TEST_DIR}" ]]; then
        rm -rf "${TEST_DIR}"
        echo "Test teardown: Removed ${TEST_DIR}"
    fi
}

# Helper function to create an old file
create_old_file() {
    local file_path="$1"
    local age_days="$2"
    touch -t "$(date -d "${age_days} days ago - 1 day" +%Y%m%d%H%M.%S)" "${file_path}"
    echo "Created old file: ${file_path} (older than ${age_days} days)"
}

# Helper function to create a new file
create_new_file() {
    local file_path="$1"
    touch "${file_path}"
    echo "Created new file: ${file_path}"
}

# Test 1: No debris found
test_no_debris() {
    setup
    create_new_file "${TEST_DIR}/new_file.txt"
    create_new_file "${TEST_DIR}/subdir/another_new_file.log"

    OUTPUT=$("${SCRIPT_PATH}" -d "${TEST_DIR}" -a 1)
    if echo "${OUTPUT}" | grep -q "No digital debris found"; then
        echo "PASS: test_no_debris"
    else
        echo "FAIL: test_no_debris - Expected 'No digital debris found', got: ${OUTPUT}"
        exit 1
    fi
    teardown
}

# Test 2: Debris found, no quarantine
test_debris_found_no_quarantine() {
    setup
    create_old_file "${TEST_DIR}/old_file.txt" 1
    create_new_file "${TEST_DIR}/new_file.txt"

    OUTPUT=$("${SCRIPT_PATH}" -d "${TEST_DIR}" -a 1)
    if echo "${OUTPUT}" | grep -q "old_file.txt" && echo "${OUTPUT}" | grep -q "To quarantine this debris"; then
        echo "PASS: test_debris_found_no_quarantine"
    else
        echo "FAIL: test_debris_found_no_quarantine - Expected old file and quarantine suggestion, got: ${OUTPUT}"
        exit 1
    fi
    teardown
}

# Test 3: Debris found and quarantined
test_debris_found_and_quarantined() {
    setup
    create_old_file "${TEST_DIR}/old_file_to_quarantine.txt" 1
    create_new_file "${TEST_DIR}/new_file.txt"

    OUTPUT=$("${SCRIPT_PATH}" -d "${TEST_DIR}" -a 1 -q)
    
    if echo "${OUTPUT}" | grep -q "Quarantined: ${TEST_DIR}/old_file_to_quarantine.txt"; then
        # Check if the file was actually moved
        if [[ ! -f "${TEST_DIR}/old_file_to_quarantine.txt" ]]; then
            QUARANTINE_SUBDIR=$(find "${TEST_DIR}" -maxdepth 1 -type d -name ".scavenger_quarantine_*" | head -n 1)
            if [[ -f "${QUARANTINE_SUBDIR}/old_file_to_quarantine.txt" ]]; then
                echo "PASS: test_debris_found_and_quarantined"
            else
                echo "FAIL: test_debris_found_and_quarantined - File not found in quarantine: ${QUARANTINE_SUBDIR}"
                exit 1
            fi
        else
            echo "FAIL: test_debris_found_and_quarantined - Old file still exists in original location."
            exit 1
        fi
    else
        echo "FAIL: test_debris_found_and_quarantined - Expected quarantine message, got: ${OUTPUT}"
        exit 1
    fi
    teardown
}

# Test 4: Invalid directory
test_invalid_directory() {
    setup
    OUTPUT=$("${SCRIPT_PATH}" -d "${TEST_DIR}/non_existent_dir" 2>&1)
    if echo "${OUTPUT}" | grep -q "Error: Target directory"; then
        echo "PASS: test_invalid_directory"
    else
        echo "FAIL: test_invalid_directory - Expected error for invalid directory, got: ${OUTPUT}"
        exit 1
    fi
    teardown
}

# Test 5: Invalid age
test_invalid_age() {
    setup
    OUTPUT=$("${SCRIPT_PATH}" -d "${TEST_DIR}" -a "zero" 2>&1)
    if echo "${OUTPUT}" | grep -q "Error: Age in days must be a positive integer"; then
        echo "PASS: test_invalid_age (non-numeric)"
    else
        echo "FAIL: test_invalid_age (non-numeric) - Expected error for invalid age, got: ${OUTPUT}"
        exit 1
    fi

    OUTPUT=$("${SCRIPT_PATH}" -d "${TEST_DIR}" -a 0 2>&1)
    if echo "${OUTPUT}" | grep -q "Error: Age in days must be a positive integer"; then
        echo "PASS: test_invalid_age (zero)"
    else
        echo "FAIL: test_invalid_age (zero) - Expected error for invalid age, got: ${OUTPUT}"
        exit 1
    fi
    teardown
}

# Test 6: No directory specified
test_no_directory_specified() {
    setup
    OUTPUT=$("${SCRIPT_PATH}" -a 1 2>&1)
    if echo "${OUTPUT}" | grep -q "Error: Target directory must be specified"; then
        echo "PASS: test_no_directory_specified"
    else
        echo "FAIL: test_no_directory_specified - Expected error for missing directory, got: ${OUTPUT}"
        exit 1
    fi
    teardown
}

# Run all tests
echo "Running tests for Nightly Digital Debris Scavenger..."
test_no_debris
test_debris_found_no_quarantine
test_debris_found_and_quarantined
test_invalid_directory
test_invalid_age
test_no_directory_specified
echo "All tests completed."
