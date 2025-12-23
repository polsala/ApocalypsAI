#!/bin/bash

# ApocalypsAI - nightly-sys-health-report - Tests

# Mocking functions and environment variables for deterministic testing

# Mock for 'command' to control availability of system commands
command() {
    local cmd="$1"
    case "$cmd" in
        "uptime") echo "mock_uptime";;
        "df") echo "mock_df";;
        "free") echo "mock_free";;
        "ps") echo "mock_ps";;
        "ping") echo "mock_ping";;
        *)
            # Default behavior: fail if not mocked
            return 1
            ;;
    esac
}

# Mock for 'uptime -p' output
mock_uptime() {
    echo "mock_uptime -p"
    echo "up 1 day, 2 hours, 30 minutes"
}

# Mock for 'df -h --output=source,pcent,target' output
mock_df() {
    echo "mock_df -h --output=source,pcent,target"
    echo "Filesystem      Size  Used Avail Use% Mounted on"
    echo "/dev/sda1       100G   85G   15G  85% /"
    echo "/dev/sdb1       200G  120G   80G  60% /home"
}

# Mock for 'free -h' output
mock_free() {
    echo "mock_free -h"
    echo "              total        used        free        shared       buff/cache   available"
    echo "Mem:           16Gi        12Gi         4Gi         1Gi         3Gi         3Gi"
    echo "Swap:           0B          0B          0B"
}

# Mock for 'ps aux --sort=-%cpu' output
mock_ps() {
    echo "mock_ps aux --sort=-%cpu"
    echo "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
    echo "root        1234 30.0  5.0 123456 78910 ?        Ss   Jan01  10:00 /usr/bin/apoc-sim --mode=apocalypse"
    echo "user        5678 15.0  2.0  98765 43210 ?        S    Jan01   5:00 /usr/bin/nightly-integrator"
    echo "root        9012  5.0  1.0  54321 21098 ?        Ss   Jan01   2:00 /usr/lib/systemd/systemd --user"
}

# Mock for 'ping -c 1 <host>'
ping() {
    local count="$1"
    local host="$2"
    if [ "$count" == "-c" ] && { [ "$host" == "8.8.8.8" ] || [ "$host" == "google.com" ]; }; then
        echo "mock_ping -c 1 $host"
        return 0 # Success
    else
        echo "mock_ping -c 1 $host"
        return 1 # Failure
    fi
}

# --- Test Execution ---

# Source the main script to run its functions in the test environment
# We need to make sure the script is in the same directory or provide a path
# For this example, assume the script is in a 'src' subdirectory relative to tests
SCRIPT_DIR=$(dirname "$0")
SOURCE_SCRIPT="${SCRIPT_DIR}/../src/main.sh"

if [ ! -f "$SOURCE_SCRIPT" ]; then
    echo "Error: Source script not found at ${SOURCE_SCRIPT}"
    exit 1
fi

# Source the script to make its functions available
. "$SOURCE_SCRIPT"

# Redirect stdout and stderr to capture output
OUTPUT=$(./src/main.sh 2>&1)

# --- Assertions ---

# Test 1: Check for header presence
if echo "$OUTPUT" | grep -q "✨ ApocalypsAI System Health Report ✨"; then
    echo "Test 1 Passed: Header is present."
else
    echo "Test 1 Failed: Header is missing."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

# Test 2: Check for uptime format
if echo "$OUTPUT" | grep -q "🚀 **System Uptime:** 1 day, 2 hours, 30 minutes"; then
    echo "Test 2 Passed: Uptime format is correct."
else
    echo "Test 2 Failed: Uptime format is incorrect."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

# Test 3: Check disk space warning for root partition
if echo "$OUTPUT" | grep -q "/dev/sda1 (/): 85% full. Uh oh, better start rationing those bits!"; then
    echo "Test 3 Passed: Root disk space warning is correct."
else
    echo "Test 3 Failed: Root disk space warning is incorrect."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

# Test 4: Check disk space normal for home partition
if echo "$OUTPUT" | grep -q "/dev/sdb1 (/home): 60% full. Plenty of room for your digital survival guides."; then
    echo "Test 4 Passed: Home disk space is normal."
else
    echo "Test 4 Failed: Home disk space is incorrect."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

# Test 5: Check memory usage display
if echo "$OUTPUT" | grep -q "Mem:           16Gi        12Gi         4Gi"; then
    echo "Test 5 Passed: Memory usage display is correct."
else
    echo "Test 5 Failed: Memory usage display is incorrect."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

# Test 6: Check top processes display
if echo "$OUTPUT" | grep -q "[1234] /usr/bin/apoc-sim --mode=apocalypse (30.0%)"; then
    echo "Test 6 Passed: Top processes display is correct."
else
    echo "Test 6 Failed: Top processes display is incorrect."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

# Test 7: Check network connectivity success
if echo "$OUTPUT" | grep -q "Ping to 8.8.8.8: Success! The digital highways are still open."; then
    echo "Test 7 Passed: Network connectivity check is successful."
else
    echo "Test 7 Failed: Network connectivity check is incorrect."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

# Test 8: Check overall status message
if echo "$OUTPUT" | grep -q "🌟 **Overall System Status:** Mostly Stable. Keep an eye on that disk space!"; then
    echo "Test 8 Passed: Overall status message is correct."
else
    echo "Test 8 Failed: Overall status message is incorrect."
    echo "--- Captured Output ---"
    echo "$OUTPUT"
    exit 1
fi

echo "All tests passed! 🎉"
exit 0
