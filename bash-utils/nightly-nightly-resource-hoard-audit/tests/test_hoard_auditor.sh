#!/bin/bash

# Test suite for nightly-resource-hoard-auditor

# Source the script to be tested
SCRIPT_TO_TEST="../src/hoard_auditor.sh"

# --- Mocking functions ---
# Mock rationale: 'du' is a system command that scans the filesystem.
# For deterministic and offline testing, we replace it with a function
# that returns predefined output.
du() {
    echo "1.2G    /var/log"
    echo "800M    /opt/data"
    echo "500M    /home/user/downloads"
    echo "200M    /usr/local"
    echo "100M    /tmp"
    echo "50M     /etc"
}

# Mock rationale: 'ps' is a system command that lists running processes.
# For deterministic and offline testing, we replace it with a function
# that returns predefined output, mimicking 'ps aux' header and data.
ps() {
    if [[ "$@" == "aux --sort=-%mem" ]]; then
        echo "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
        echo "root           1  0.0  5.0 123456 65432 ?        Ss   Jan01   0:01 /usr/bin/hoarder-app --mem-hog"
        echo "user       10001  0.0  3.5 98765  43210 pts/0    Sl   Feb01   0:05 /usr/bin/another-app"
        echo "daemon     20002  0.0  2.0 54321  21098 ?        S    Mar01   0:02 /usr/sbin/background-service"
        echo "root           2  0.0  1.5 1234   5678 ?        S    Jan01   0:00 [kthreadd]"
        echo "user       10002  0.0  1.0 1111   2222 pts/1    R+   Apr01   0:00 bash"
        echo "root           3  0.0  0.5 999    1111 ?        S    Jan01   0:00 [rcu_gp]"
    elif [[ "$@" == "aux --sort=-%cpu" ]]; then
        echo "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
        echo "user       10003 15.0  0.5 12345  67890 pts/0    R    May01   0:10 /usr/bin/cpu-burner --intensive"
        echo "root           4  8.0  0.2 9876   5432 ?        R    Jan01   0:08 [ksoftirqd/0]"
        echo "user       10004  5.0  0.1 5432   1000 pts/1    S    Jun01   0:03 /usr/bin/idle-process"
        echo "root           5  2.0  0.1 1111   2222 ?        S    Jan01   0:01 [migration/0]"
        echo "user       10005  1.0  0.1 999    1111 pts/2    S    Jul01   0:00 sleep 60"
        echo "root           6  0.5  0.1 888    999 ?        S    Jan01   0:00 [cpuhp/0]"
    else
        # Fallback for other ps calls if any
        /bin/ps "$@"
    fi
}

# --- Test functions ---

test_output_contains_headers() {
    local output
    output=$(bash "$SCRIPT_TO_TEST")

    if ! echo "$output" | grep -q "ApocalypsAI Resource Hoard Auditor Report"; then
        echo "FAIL: Output missing main report header."
        return 1
    fi
    if ! echo "$output" | grep -q "--- \[ Sector: Disk Hoards"; then
        echo "FAIL: Output missing Disk Hoards header."
        return 1
    fi
    if ! echo "$output" | grep -q "--- \[ Sector: Memory Hoards"; then
        echo "FAIL: Output missing Memory Hoards header."
        return 1
    fi
    if ! echo "$output" | grep -q "--- \[ Sector: CPU Hoards"; then
        echo "FAIL: Output missing CPU Hoards header."
        return 1
    fi
    if ! echo "$output" | grep -q "Audit Complete. May your resources be ever balanced."; then
        echo "FAIL: Output missing audit completion message."
        return 1
    fi
    echo "PASS: All expected headers and footers are present."
    return 0
}

test_disk_hoards_output() {
    local output
    output=$(bash "$SCRIPT_TO_TEST")

    if ! echo "$output" | grep -q "1.2G    /var/log"; then
        echo "FAIL: Disk hoards output missing expected entry for /var/log."
        return 1
    fi
    if ! echo "$output" | grep -q "800M    /opt/data"; then
        echo "FAIL: Disk hoards output missing expected entry for /opt/data."
        return 1
    fi
    # Ensure only top 5 are shown (based on mock data)
    if echo "$output" | grep -q "50M     /etc"; then
        echo "FAIL: Disk hoards output showing more than top 5 entries."
        return 1
    fi
    echo "PASS: Disk hoards section contains expected top entries."
    return 0
}

test_memory_hoards_output() {
    local output
    output=$(bash "$SCRIPT_TO_TEST")

    if ! echo "$output" | grep -q "5.0 123456 65432 ?        Ss   Jan01   0:01 /usr/bin/hoarder-app --mem-hog"; then
        echo "FAIL: Memory hoards output missing expected entry for hoarder-app."
        return 1
    fi
    if ! echo "$output" | grep -q "3.5 98765  43210 pts/0    Sl   Feb01   0:05 /usr/bin/another-app"; then
        echo "FAIL: Memory hoards output missing expected entry for another-app."
        return 1
    fi
    # Ensure only top 5 processes + header are shown (6 lines total from ps mock)
    if echo "$output" | grep -q "0.5 999    1111 ?        S    Jan01   0:00 \[rcu_gp\]"; then
        echo "FAIL: Memory hoards output showing more than top 5 processes."
        return 1
    fi
    echo "PASS: Memory hoards section contains expected top entries."
    return 0
}

test_cpu_hoards_output() {
    local output
    output=$(bash "$SCRIPT_TO_TEST")

    if ! echo "$output" | grep -q "15.0  0.5 12345  67890 pts/0    R    May01   0:10 /usr/bin/cpu-burner --intensive"; then
        echo "FAIL: CPU hoards output missing expected entry for cpu-burner."
        return 1
    fi
    if ! echo "$output" | grep -q "8.0  0.2 9876   5432 ?        R    Jan01   0:08 \[ksoftirqd/0\]"; then
        echo "FAIL: CPU hoards output missing expected entry for ksoftirqd/0."
        return 1
    fi
    # Ensure only top 5 processes + header are shown (6 lines total from ps mock)
    if echo "$output" | grep -q "0.5  0.1 888    999 ?        S    Jan01   0:00 \[cpuhp/0\]"; then
        echo "FAIL: CPU hoards output showing more than top 5 processes."
        return 1
    fi
    echo "PASS: CPU hoards section contains expected top entries."
    return 0
}

# --- Run all tests ---
echo "Running tests for $SCRIPT_TO_TEST..."
test_output_contains_headers
test_disk_hoards_output
test_memory_hoards_output
test_cpu_hoards_output
echo "All tests complete."
