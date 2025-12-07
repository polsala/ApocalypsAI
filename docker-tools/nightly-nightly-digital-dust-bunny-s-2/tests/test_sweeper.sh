#!/bin/bash

# Tests for Digital Dust Bunny Sweeper
# Mock rationale: We create a temporary test environment to verify the sweeper works correctly

set -e

# Create temporary test directory
TEST_DIR="/tmp/dust_bunny_test"
TEST_SCAN_DIR="$TEST_DIR/scan"
TEST_CONFIG_DIR="$TEST_DIR/config"

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}

# Setup test environment
setup() {
    cleanup
    mkdir -p "$TEST_SCAN_DIR"
    mkdir -p "$TEST_CONFIG_DIR"
    
    # Create test files and directories
    mkdir -p "$TEST_SCAN_DIR/empty_dir"
    mkdir -p "$TEST_SCAN_DIR/normal_dir"
    echo "content" > "$TEST_SCAN_DIR/normal_dir/file.txt"
    echo "cache" > "$TEST_SCAN_DIR/stale.cache"
    echo "tmp" > "$TEST_SCAN_DIR/temp.tmp"
    echo "log" > "$TEST_SCAN_DIR/app.log"
    
    # Make files old (simulate 31 days old)
    touch -d "31 days ago" "$TEST_SCAN_DIR/stale.cache"
    touch -d "31 days ago" "$TEST_SCAN_DIR/temp.tmp"
    touch -d "31 days ago" "$TEST_SCAN_DIR/app.log"
    
    # Create config file
    cat > "$TEST_CONFIG_DIR/config.json" << EOF
{
  "scan_paths": ["$TEST_SCAN_DIR"],
  "min_age_days": 30,
  "report_format": "text"
}
EOF
}

# Test 1: Basic functionality
test_basic_scan() {
    echo "Running basic scan test..."
    
    # Run the sweeper
    docker build -t dust-bunny-sweeper . > /dev/null 2>&1
    docker run --rm -v "$TEST_SCAN_DIR:/scan" dust-bunny-sweeper > /dev/null
    
    # Check if report was generated
    if [[ -f "$TEST_SCAN_DIR/dust_bunny_report.txt" ]]; then
        echo "✓ Report file generated"
    else
        echo "✗ Report file not found"
        return 1
    fi
    
    # Check report content
    if grep -q "Empty Directory: $TEST_SCAN_DIR/empty_dir" "$TEST_SCAN_DIR/dust_bunny_report.txt"; then
        echo "✓ Empty directory detected"
    else
        echo "✗ Empty directory not detected"
        return 1
    fi
    
    if grep -q "Stale Cache: $TEST_SCAN_DIR/stale.cache" "$TEST_SCAN_DIR/dust_bunny_report.txt"; then
        echo "✓ Stale cache file detected"
    else
        echo "✗ Stale cache file not detected"
        return 1
    fi
}

# Test 2: JSON format
test_json_format() {
    echo "Running JSON format test..."
    
    # Run the sweeper with JSON format
    docker run --rm -e REPORT_FORMAT=json -v "$TEST_SCAN_DIR:/scan" dust-bunny-sweeper > /dev/null
    
    # Check if JSON report was generated
    if [[ -f "$TEST_SCAN_DIR/dust_bunny_report.json" ]]; then
        echo "✓ JSON report file generated"
    else
        echo "✗ JSON report file not found"
        return 1
    fi
    
    # Check JSON validity
    if python3 -m json.tool "$TEST_SCAN_DIR/dust_bunny_report.json" > /dev/null; then
        echo "✓ JSON report is valid"
    else
        echo "✗ JSON report is invalid"
        return 1
    fi
}

# Test 3: Configuration file
test_config_file() {
    echo "Running config file test..."
    
    # Run the sweeper with config file
    docker run --rm -v "$TEST_SCAN_DIR:/scan" -v "$TEST_CONFIG_DIR:/config" dust-bunny-sweeper /scan /config/config.json > /dev/null
    
    # Check if report was generated
    if [[ -f "$TEST_SCAN_DIR/dust_bunny_report.txt" ]]; then
        echo "✓ Report generated with config file"
    else
        echo "✗ Report not generated with config file"
        return 1
    fi
}

# Run tests
main() {
    echo "Starting Digital Dust Bunny Sweeper tests..."
    setup
    
    test_basic_scan
    test_json_format
    test_config_file
    
    cleanup
    echo "All tests passed! ✓"
}

# Execute tests
main
