#!/bin/bash

# Test suite for Nightly Bash Uptime Emoji 2
# Uses mocks to ensure deterministic, offline testing

set -euo pipefail

# Source the main script functions (without executing main)
# We'll extract and test individual functions

# Mock rationale: Simulate different uptime scenarios for testing
mock_uptime_seconds() {
    local scenario=$1
    case $scenario in
        "fresh") echo 300 ;;      # 5 minutes
        "hour") echo 7200 ;;      # 2 hours
        "day") echo 90000 ;;     # 1 day + 1 hour
        "week") echo 604800 ;;   # 1 week
        "long") echo 2592000 ;;   # 30 days
        *) echo 3600 ;;           # Default 1 hour
    esac
}

# Test formatting uptime
test_format_uptime() {
    echo "Testing format_uptime function..."
    
    # Test 5 minutes
    local uptime_1=$(mock_uptime_seconds "fresh")
    local formatted_1=$(bash -c "source src/main.sh; format_uptime $uptime_1")
    echo "  5 minutes: $formatted_1"
    
    # Test 2 hours
    local uptime_2=$(mock_uptime_seconds "hour")
    local formatted_2=$(bash -c "source src/main.sh; format_uptime $uptime_2")
    echo "  2 hours: $formatted_2"
    
    # Test 1 day + 1 hour
    local uptime_3=$(mock_uptime_seconds "day")
    local formatted_3=$(bash -c "source src/main.sh; format_uptime $uptime_3")
    echo "  1 day + 1 hour: $formatted_3"
    
    # Test 1 week
    local uptime_4=$(mock_uptime_seconds "week")
    local formatted_4=$(bash -c "source src/main.sh; format_uptime $uptime_4")
    echo "  1 week: $formatted_4"
    
    # Test 30 days
    local uptime_5=$(mock_uptime_seconds "long")
    local formatted_5=$(bash -c "source src/main.sh; format_uptime $uptime_5")
    echo "  30 days: $formatted_5"
    
    echo "✓ format_uptime tests completed"
}

# Test progress bar creation
test_progress_bar() {
    echo "\nTesting progress_bar function..."
    
    # Test various percentages
    for percentage in 0 25 50 75 100; do
        echo -n "  $percentage%: "
        bash -c "source src/main.sh; create_progress_bar $percentage"
        echo ""
    done
    
    echo "✓ progress_bar tests completed"
}

# Test ASCII art display
test_ascii_art() {
    echo "\nTesting ASCII art display..."
    
    # Test fresh system (< 1 day)
    echo "  Fresh system (< 1 day):"
    bash -c "source src/main.sh; show_ascii_art $(mock_uptime_seconds "fresh")"
    
    # Test day-old system
    echo "  Day-old system (>= 1 day):"
    bash -c "source src/main.sh; show_ascii_art $(mock_uptime_seconds "day")"
    
    # Test week-old system
    echo "  Week-old system (>= 7 days):"
    bash -c "source src/main.sh; show_ascii_art $(mock_uptime_seconds "week")"
    
    echo "✓ ASCII art tests completed"
}

# Test encouragement messages
test_encouragement() {
    echo "\nTesting encouragement messages..."
    
    # Test various uptime scenarios
    local scenarios=("fresh" "hour" "day" "week" "long")
    for scenario in "${scenarios[@]}"; do
        local uptime=$(mock_uptime_seconds "$scenario")
        local message=$(bash -c "source src/main.sh; get_encouragement $uptime")
        echo "  $scenario system: $message"
    done
    
    echo "✓ encouragement tests completed"
}

# Test uptime percentage calculation
test_uptime_percentage() {
    echo "\nTesting uptime percentage calculation..."
    
    # Test various uptime scenarios
    local scenarios=("fresh" "hour" "day" "week" "long")
    for scenario in "${scenarios[@]}"; do
        local uptime=$(mock_uptime_seconds "$scenario")
        local percentage=$(bash -c "source src/main.sh; get_uptime_percentage $uptime")
        echo "  $scenario system ($uptime seconds): ${percentage}%"
    done
    
    echo "✓ uptime percentage tests completed"
}

# Test script execution
test_script_execution() {
    echo "\nTesting full script execution..."
    
    # Mock the get_uptime_seconds function to return a fixed value
    # This ensures consistent testing
    local mock_uptime=90000  # 1 day + 1 hour
    
    # Run the script with mocked uptime
    echo "  Running with mocked uptime of $mock_uptime seconds..."
    
    # Create a temporary script with mocked uptime
    cat > /tmp/test_uptime.sh << EOF
#!/bin/bash
source src/main.sh

# Override get_uptime_seconds for testing
get_uptime_seconds() {
    echo $mock_uptime
}

# Run main with mocked uptime
main
EOF

    chmod +x /tmp/test_uptime.sh
    /tmp/test_uptime.sh
    rm /tmp/test_uptime.sh
    
    echo "✓ script execution test completed"
}

# Run all tests
main_test() {
    echo "=== Nightly Bash Uptime Emoji 2 - Test Suite ===\n"
    
    test_format_uptime
    test_progress_bar
    test_ascii_art
    test_encouragement
    test_uptime_percentage
    test_script_execution
    
    echo "\n🎉 All tests completed successfully!"
}

# Run the test suite
main_test
