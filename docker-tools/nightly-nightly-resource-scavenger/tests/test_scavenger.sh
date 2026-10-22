#!/bin/bash
set -euo pipefail

# Mock rationale: Create a temporary environment with mocked `docker` and `date` commands
# to ensure deterministic and offline testing of the scavenger script's logic.

# Create a temporary directory for mock executables
TEST_DIR=$(mktemp -d)
MOCK_BIN_DIR="$TEST_DIR/bin"
mkdir -p "$MOCK_BIN_DIR"

# Create mock docker command script
cat << 'EOF' > "$MOCK_BIN_DIR/docker"
#!/bin/bash
# Mock rationale: Simulate docker commands for offline, deterministic testing.

if [[ "$1" == "ps" && "$2" == "-a" && "$3" == "--format" ]]; then
    # Mock output for 'docker ps -a'
    echo -e "mock_id_stale_1\tstale-container-1\tExited (0) 20 hours ago\t2023-10-22 10:00:00 +0000 UTC"
    echo -e "mock_id_stale_2\tstale-container-2\tExited (0) 8 days ago\t2023-10-15 10:00:00 +0000 UTC"
    echo -e "mock_id_running_1\trunning-container-1\tUp 5 hours\t2023-10-22 15:00:00 +0000 UTC"
    echo -e "mock_id_running_2\trunning-container-2\tUp 10 minutes\t2023-10-23 00:00:00 +0000 UTC"
    echo -e "mock_id_stale_3\tstale-container-3\tExited (1) 15 days ago\t2023-10-08 10:00:00 +0000 UTC"
elif [[ "$1" == "stats" && "$2" == "--no-stream" && "$3" == "--format" ]]; then
    # Mock output for 'docker stats --no-stream'
    # Only running containers appear in stats
    echo -e "mock_id_running_1\trunning-container-1\t95.00%\t1.8GiB / 2GiB\t90.00%"
    echo -e "mock_id_running_2\trunning-container-2\t5.00%\t100MiB / 1GiB\t10.00%"
else
    echo "Mock docker: Unknown command: $@" >&2
    exit 1
fi
EOF
chmod +x "$MOCK_BIN_DIR/docker"

# Create mock date command script
cat << 'EOF' > "$MOCK_BIN_DIR/date"
#!/bin/bash
# Mock rationale: Simulate date command for deterministic time calculations in tests.

if [[ "$1" == "+%s" ]]; then
    echo "1698091200" # Fixed timestamp for 2023-10-23 12:00:00 UTC
elif [[ "$1" == "-d" && "$3" == "+%s" ]]; then
    case "$2" in
        "2023-10-22 10:00:00 UTC") echo "1698055200" ;; # 2023-10-22 10:00:00 UTC (1 day, 2 hours before fixed current time)
        "2023-10-15 10:00:00 UTC") echo "1697364000" ;; # 2023-10-15 10:00:00 UTC (8 days, 2 hours before fixed current time)
        "2023-10-22 15:00:00 UTC") echo "1698073200" ;; # 2023-10-22 15:00:00 UTC (21 hours before fixed current time)
        "2023-10-23 00:00:00 UTC") echo "1698091200" ;; # 2023-10-23 00:00:00 UTC (12 hours before fixed current time)
        "2023-10-08 10:00:00 UTC") echo "1696759200" ;; # 2023-10-08 10:00:00 UTC (15 days, 2 hours before fixed current time)
        *) echo "Mock date: Unknown date string: $2" >&2; exit 1 ;;
    esac
elif [[ "$1" == "-u" ]]; then
    echo "Mon Oct 23 12:00:00 UTC 2023" # Fixed date string for report header
else
    echo "Mock date: Unknown command: $@" >&2
    exit 1
fi
EOF
chmod +x "$MOCK_BIN_DIR/date"

# Set PATH to use our mock commands first
export PATH="$MOCK_BIN_DIR:$PATH"

echo "Running tests for nightly-resource-scavenger..."

# --- Test Case 1: Default thresholds ---
# CPU > 80%, Mem > 80%, Stale > 7 days
echo "\n--- Test Case 1: Default thresholds (CPU > 80%, Mem > 80%, Stale > 7 days) ---"
OUTPUT=$(bash ../src/scavenge.sh)

# Expected: stale-container-2 (8 days old) and stale-container-3 (15 days old) should be detected.
# Expected: running-container-1 (CPU 95%, Mem 90%) should be detected.
# Expected: stale-container-1 (20 hours old) and running-container-2 (CPU 5%, Mem 10%) should NOT be detected.

if echo "$OUTPUT" | grep -q "stale-container-2"; then
    echo "PASS: stale-container-2 (8 days old) detected."
else
    echo "FAIL: stale-container-2 (8 days old) not detected."
    exit 1
fi

if echo "$OUTPUT" | grep -q "stale-container-3"; then
    echo "PASS: stale-container-3 (15 days old) detected."
else
    echo "FAIL: stale-container-3 (15 days old) not detected."
    exit 1
fi

if echo "$OUTPUT" | grep -q "running-container-1"; then
    echo "PASS: running-container-1 (CPU 95%, Mem 90%) detected."
else
    echo "FAIL: running-container-1 (CPU 95%, Mem 90%) not detected."
    exit 1
fi

if echo "$OUTPUT" | grep -q "stale-container-1" && ! echo "$OUTPUT" | grep -q "No stale containers found."; then
    echo "FAIL: stale-container-1 (20 hours old) incorrectly reported as stale."
    exit 1
else
    echo "PASS: stale-container-1 (20 hours old) not reported as stale."
fi

if echo "$OUTPUT" | grep -q "running-container-2" && ! echo "$OUTPUT" | grep -q "No resource-hungry containers found."; then
    echo "FAIL: running-container-2 (CPU 5%, Mem 10%) incorrectly reported as hungry."
    exit 1
else
    echo "PASS: running-container-2 (CPU 5%, Mem 10%) not reported as hungry."
fi

# --- Test Case 2: Custom thresholds ---
# CPU > 50%, Mem > 5%, Stale > 1 day
echo "\n--- Test Case 2: Custom thresholds (CPU > 50%, Mem > 5%, Stale > 1 day) ---"
OUTPUT=$(bash ../src/scavenge.sh --cpu-threshold 50 --mem-threshold 5 --stale-days 1)

# Expected: stale-container-1 (20 hours old) should now be detected with 1-day threshold.
# Expected: running-container-1 (CPU 95%, Mem 90%) should still be detected with 50% CPU threshold.
# Expected: running-container-2 (CPU 5%, Mem 10%) should now be detected with 5% Mem threshold.

if echo "$OUTPUT" | grep -q "stale-container-1"; then
    echo "PASS: stale-container-1 (20 hours old) detected with 1-day threshold."
else
    echo "FAIL: stale-container-1 (20 hours old) not detected with 1-day threshold."
    exit 1
fi

if echo "$OUTPUT" | grep -q "running-container-1"; then
    echo "PASS: running-container-1 (CPU 95%, Mem 90%) detected with 50% CPU threshold."
else
    echo "FAIL: running-container-1 (CPU 95%, Mem 90%) not detected with 50% CPU threshold."
    exit 1
fi

if echo "$OUTPUT" | grep -q "running-container-2"; then
    echo "PASS: running-container-2 (CPU 5%, Mem 10%) detected with 5% Mem threshold."
else
    echo "FAIL: running-container-2 (CPU 5%, Mem 10%) not detected with 5% Mem threshold."
    exit 1
fi

echo "\nAll tests passed!"

# Clean up mock environment
rm -rf "$TEST_DIR"
