#!/bin/bash

# Source the main script to access its functions
. src/serenity_sensor.sh

# --- Test Utilities ---
assert_contains() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"
    if echo "$actual" | grep -qF "$expected"; then
        echo "✅ PASS: $test_name (contains '$expected')"
    else
        echo "❌ FAIL: $test_name (expected to contain '$expected', but got:\n$actual)"
        exit 1
    fi
}

assert_not_contains() {
    local unexpected="$1"
    local actual="$2"
    local test_name="$3"
    if ! echo "$actual" | grep -qF "$unexpected"; then
        echo "✅ PASS: $test_name (does not contain '$unexpected')"
    else
        echo "❌ FAIL: $test_name (expected NOT to contain '$unexpected', but got:\n$actual)"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: All serene
test_all_serene() {
    echo "--- Running Test: All Serene ---"
    # Mock rationale: Simulate a perfectly healthy system for deterministic testing.
    get_disk_usage() { echo "10"; }
    get_mem_usage() { echo "20"; }
    get_load_average() { echo "0.10"; }
    is_service_active() { return 0; } # All services active

    local output=$(generate_serenity_report)
    assert_contains "✅ Disk Serenity: PEACEFUL." "$output" "Disk Serene"
    assert_contains "✅ Memory Serenity: PEACEFUL." "$output" "Memory Serene"
    assert_contains "✅ CPU Load Serenity: PEACEFUL." "$output" "CPU Load Serene"
    assert_contains "✅ Service 'sshd': Active." "$output" "Service sshd Active"
    assert_contains "✅ Service 'cron': Active." "$output" "Service cron Active"
    assert_contains "✨ Overall System Serenity: ALL IS WELL." "$output" "Overall Serene"
    echo ""
}

# Test 2: Disk stressed
test_disk_stressed() {
    echo "--- Running Test: Disk Stressed ---"
    # Mock rationale: Simulate high disk usage to trigger the 'stressed' warning.
    get_disk_usage() { echo "85"; }
    get_mem_usage() { echo "20"; }
    get_load_average() { echo "0.10"; }
    is_service_active() { return 0; }

    local output=$(generate_serenity_report)
    assert_contains "⚠️ Disk Serenity: STRESSED. Disk space is at 85%." "$output" "Disk Stressed"
    assert_contains "⚡ Overall System Serenity: CONCERNS DETECTED." "$output" "Overall Concerns"
    echo ""
}

# Test 3: Memory critical
test_mem_critical() {
    echo "--- Running Test: Memory Critical ---"
    # Mock rationale: Simulate very high memory usage to trigger the 'critical' alert.
    get_disk_usage() { echo "10"; }
    get_mem_usage() { echo "95"; }
    get_load_average() { echo "0.10"; }
    is_service_active() { return 0; }

    local output=$(generate_serenity_report)
    assert_contains "🚨 Memory Serenity: CRITICAL! Memory usage is at 95%!" "$output" "Memory Critical"
    assert_contains "⚡ Overall System Serenity: CONCERNS DETECTED." "$output" "Overall Concerns"
    echo ""
}

# Test 4: CPU load critical
test_cpu_critical() {
    echo "--- Running Test: CPU Critical ---"
    # Mock rationale: Simulate high CPU load to trigger the 'critical' alert.
    get_disk_usage() { echo "10"; }
    get_mem_usage() { echo "20"; }
    get_load_average() { echo "6.50"; } # Above 5.0 critical threshold
    is_service_active() { return 0; }

    local output=$(generate_serenity_report)
    assert_contains "🚨 CPU Load Serenity: CRITICAL! 1-min load average is 6.50!" "$output" "CPU Critical"
    assert_contains "⚡ Overall System Serenity: CONCERNS DETECTED." "$output" "Overall Concerns"
    echo ""
}

# Test 5: Service inactive
test_service_inactive() {
    echo "--- Running Test: Service Inactive ---"
    # Mock rationale: Simulate a critical service being inactive.
    get_disk_usage() { echo "10"; }
    get_mem_usage() { echo "20"; }
    get_load_average() { echo "0.10"; }
    is_service_active() {
        local service_name="$1"
        if [[ "$service_name" == "sshd" ]]; then
            return 1 # sshd is inactive
        else
            return 0 # cron is active
        fi
    }

    local output=$(generate_serenity_report)
    assert_contains "🚨 Service 'sshd': INACTIVE!" "$output" "Service sshd Inactive"
    assert_contains "✅ Service 'cron': Active." "$output" "Service cron Active"
    assert_contains "⚡ Overall System Serenity: CONCERNS DETECTED." "$output" "Overall Concerns"
    echo ""
}

# Test 6: Custom thresholds via environment variables
test_custom_thresholds() {
    echo "--- Running Test: Custom Thresholds ---"
    # Mock rationale: Test that environment variables correctly override default thresholds.
    DISK_THRESHOLD_CRITICAL=50
    DISK_THRESHOLD_STRESSED=40

    get_disk_usage() { echo "45"; } # Should be stressed with new threshold
    get_mem_usage() { echo "20"; }
    get_load_average() { echo "0.10"; }
    is_service_active() { return 0; }

    local output=$(generate_serenity_report)
    assert_contains "⚠️ Disk Serenity: STRESSED. Disk space is at 45%." "$output" "Custom Disk Stressed"
    assert_contains "⚡ Overall System Serenity: CONCERNS DETECTED." "$output" "Overall Concerns with Custom Thresholds"

    # Reset thresholds for subsequent tests
    unset DISK_THRESHOLD_CRITICAL
    unset DISK_THRESHOLD_STRESSED
    echo ""
}

# Run all tests
test_all_serene
test_disk_stressed
test_mem_critical
test_cpu_critical
test_service_inactive
test_custom_thresholds

echo "All tests completed."
