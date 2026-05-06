#!/bin/bash

# ApocalypsAI - Nightly System Health Reporter Tests
# Classifier: bash-utils

# Mock rationale: These mocks simulate the output of system commands to ensure the script's parsing and logic are correct without relying on actual system state.

# --- Mock Functions ---

mock_top() {
    echo "top - 10:00:00 up 10 days,  1:23,  2 users,  load average: 0.10, 0.15, 0.20"
    echo "Tasks: 200 total,   1 running, 199 sleeping,   0 stopped,   0 zombie"
    echo "%Cpu(s): 10.0 us,  2.0 sy,  0.0 ni, 87.0 id,  1.0 wa,  0.0 hi,  0.0 si,  0.0 st"
    echo "MiB Mem :  16000.0 total,   8000.0 free,   4000.0 used,   4000.0 buff/cache"
    echo "MiB Swap:   2000.0 total,   1500.0 free,    500.0 used.  10000.0 avail Mem"
}

mock_free() {
    echo "              total        used        free      shared  buff/cache   available"
    echo "Mem:         16000000     4000000     8000000      100000     4000000    10000000"
    echo "Swap:         2000000      500000     1500000"
}

mock_df() {
    echo "Filesystem      Size  Used Avail Use% Mounted on"
    echo "/dev/sda1        50G   40G   10G  80% /"
    echo "tmpfs           7.8G     0  7.8G   0% /dev/shm"
    echo "/dev/sdb1       200G  180G   20G  90% /data"
}

mock_ps() {
    echo "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
    echo "root           1  0.0  0.1 168000 10000 ?        Ss   Jan01   0:01 /sbin/init"
    echo "user        1234 15.0  5.0 500000 200000 ?       Sl   10:00   1:30 /usr/bin/heavy_process"
    echo "user        5678  5.0  2.0 300000 100000 ?       Sl   10:05   0:45 /usr/bin/another_process"
    echo "root        9012  1.0  1.0 200000  50000 ?       S    10:10   0:10 /usr/sbin/system_service"
    echo "user        3456  0.5  0.5 100000  25000 ?       S    10:15   0:05 /usr/bin/utility_process"
}

mock_ss() {
    echo "Netid State  Recv-Q Send-Q Local Address:Port Peer Address:Port"
    echo "tcp   LISTEN 0      128    0.0.0.0:22       0.0.0.0:*
    echo "tcp   LISTEN 0      128       [::]:22          [::]:*"
    echo "tcp   LISTEN 0      100    127.0.0.1:631      0.0.0.0:*
    echo "tcp   LISTEN 0      128       [::]:631         [::]:*"
    echo "tcp   ESTAB  0      0    192.168.1.100:45678  192.168.1.1:80"
}

# --- Test Runner ---

run_test() {
    TEST_NAME="$1"
    EXPECTED_OUTPUT="$2"
    COMMAND_TO_RUN="$3"

    echo "Running test: $TEST_NAME"

    # Temporarily replace actual commands with mocks
    ORIGINAL_TOP="$(type -p top)"
    ORIGINAL_FREE="$(type -p free)"
    ORIGINAL_DF="$(type -p df)"
    ORIGINAL_PS="$(type -p ps)"
    ORIGINAL_SS="$(type -p ss)"

    alias top='mock_top'
    alias free='mock_free'
    alias df='mock_df'
    alias ps='mock_ps'
    alias ss='mock_ss'

    # Execute the script and capture output
    ACTUAL_OUTPUT=$(eval "$COMMAND_TO_RUN")

    # Restore original commands
    unalias top
    unalias free
    unalias df
    unalias ps
    unalias ss

    # Compare output (ignoring dynamic parts like date and exact process PIDs if needed)
    # For simplicity, we'll do a basic string comparison here.
    # A more robust test would parse the output and compare specific fields.
    if echo "$ACTUAL_OUTPUT" | grep -q "$(echo "$EXPECTED_OUTPUT" | sed 's/[0-9.]*%/.*%/g')"; then
        echo "  PASS: $TEST_NAME"
    else
        echo "  FAIL: $TEST_NAME"
        echo "    Expected (partial): $(echo "$EXPECTED_OUTPUT" | head -n 5)"
        echo "    Actual (partial): $(echo "$ACTUAL_OUTPUT" | head -n 5)"
        return 1
    fi
    return 0
}

# --- Test Cases ---

# Test 1: Basic report structure and CPU metric
run_test "CPU Metric Reporting" "CPU Load" "./nightly-sys-health-reporter.sh"
if [ $? -ne 0 ]; then exit 1; fi

# Test 2: Memory metric reporting
run_test "Memory Metric Reporting" "RAM Usage" "./nightly-sys-health-reporter.sh"
if [ $? -ne 0 ]; then exit 1; fi

# Test 3: Disk space reporting
run_test "Disk Space Reporting" "/dev/sda1        50G   40G   10G  80% /" "./nightly-sys-health-reporter.sh"
if [ $? -ne 0 ]; then exit 1; fi

# Test 4: Top processes reporting
run_test "Top Processes Reporting" "1234 15.0  5.0 500000 200000 ?       Sl" "./nightly-sys-health-reporter.sh"
if [ $? -ne 0 ]; then exit 1; fi

# Test 5: Network connections reporting
run_test "Network Connections Reporting" "tcp   ESTAB  0      0    192.168.1.100:45678  192.168.1.1:80" "./nightly-sys-health-reporter.sh"
if [ $? -ne 0 ]; then exit 1; fi

# Test 6: Warning condition for high CPU

mock_top() {
    echo "top - 10:00:00 up 10 days,  1:23,  2 users,  load average: 0.10, 0.15, 0.20"
    echo "Tasks: 200 total,   1 running, 199 sleeping,   0 stopped,   0 zombie"
    echo "%Cpu(s): 90.0 us,  2.0 sy,  0.0 ni,  8.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st"
    echo "MiB Mem :  16000.0 total,   8000.0 free,   4000.0 used,   4000.0 buff/cache"
    echo "MiB Swap:   2000.0 total,   1500.0 free,    500.0 used.  10000.0 avail Mem"
}
run_test "High CPU Warning" "The processors are groaning under the strain" "./nightly-sys-health-reporter.sh"
if [ $? -ne 0 ]; then exit 1; fi

# Test 7: Warning condition for low disk space

mock_df() {
    echo "Filesystem      Size  Used Avail Use% Mounted on"
    echo "/dev/sda1        50G   45G    5G  90% /"
    echo "tmpfs           7.8G     0  7.8G   0% /dev/shm"
    echo "/dev/sdb1       200G  180G   20G  90% /data"
}
run_test "Low Disk Space Warning" "Storage is becoming scarce" "./nightly-sys-health-reporter.sh"
if [ $? -ne 0 ]; then exit 1; fi



echo "All tests passed! System health reporting is operational."
exit 0
