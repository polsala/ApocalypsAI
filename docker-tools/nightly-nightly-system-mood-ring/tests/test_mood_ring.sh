#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the image name
IMAGE_NAME="system-mood-ring-test"

# --- Mock Rationale ---
# The mood_ring.sh script reads system metrics from /proc/stat and /proc/meminfo.
# To make tests deterministic and offline, we provide mock versions of these files.
# The script is designed to accept an environment variable PROC_ROOT which, if set,
# will prepend to the /proc paths (e.g., $PROC_ROOT/stat instead of /proc/stat).
# This allows the test script to create temporary directories with mock files and
# point PROC_ROOT to them, ensuring the script processes predefined system states.

# Create a temporary directory for mock /proc files
MOCK_PROC_DIR=$(mktemp -d)
trap "rm -rf $MOCK_PROC_DIR" EXIT # Clean up on exit

# Function to create mock /proc files
create_mock_proc_files() {
    local base_dir=$1
    mkdir -p "$base_dir"

    # Mock /proc/stat (values are jiffies, 100 per second)
    # Total jiffies = user+nice+system+idle+iowait+irq+softirq+steal
    # Idle jiffies = idle+iowait

    # Low usage: 10% CPU
    # Total: 1000, Idle: 900, Used: 100
    # cpu 100 0 0 900 0 0 0 0 0 0
    cat <<EOF > "$base_dir/stat_low"
cpu 100 0 0 900 0 0 0 0 0 0
cpu0 100 0 0 900 0 0 0 0 0 0
EOF

    # Moderate usage: 50% CPU
    # Total: 1000, Idle: 500, Used: 500
    # cpu 500 0 0 500 0 0 0 0 0 0
    cat <<EOF > "$base_dir/stat_moderate"
cpu 500 0 0 500 0 0 0 0 0 0
cpu0 500 0 0 500 0 0 0 0 0 0
EOF

    # High usage: 80% CPU
    # Total: 1000, Idle: 200, Used: 800
    # cpu 800 0 0 200 0 0 0 0 0 0
    cat <<EOF > "$base_dir/stat_high"
cpu 800 0 0 200 0 0 0 0 0 0
cpu0 800 0 0 200 0 0 0 0 0 0
EOF

    # Mock /proc/meminfo (values in kB)
    # Low usage: 20% Memory used (80% available)
    # Total: 100000, Available: 80000, Used: 20000
    cat <<EOF > "$base_dir/meminfo_low"
MemTotal:       100000 kB
MemFree:         10000 kB
MemAvailable:    80000 kB
EOF

    # Moderate usage: 50% Memory used (50% available)
    # Total: 100000, Available: 50000, Used: 50000
    cat <<EOF > "$base_dir/meminfo_moderate"
MemTotal:       100000 kB
MemFree:         10000 kB
MemAvailable:    50000 kB
EOF

    # High usage: 90% Memory used (10% available)
    # Total: 100000, Available: 10000, Used: 90000
    cat <<EOF > "$base_dir/meminfo_high"
MemTotal:       100000 kB
MemFree:         10000 kB
MemAvailable:    10000 kB
EOF
}

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" . > /dev/null
echo "Docker image built successfully."

# Function to run a test case
run_test_case() {
    local test_name=$1
    local stat_file_path=$2
    local meminfo_file_path=$3
    local expected_output_regex=$4

    echo "--- Running test: $test_name ---"

    # Create a unique mock_proc directory for this test run
    local current_mock_proc_dir="$MOCK_PROC_DIR/test_$(date +%s%N)"
    mkdir -p "$current_mock_proc_dir"
    cp "$stat_file_path" "$current_mock_proc_dir/stat"
    cp "$meminfo_file_path" "$current_mock_proc_dir/meminfo"

    # Run the container, capture output for a short period (2 iterations for CPU calculation)
    # We need to run it twice for CPU calculation to work (needs prev values).
    # The first output will show 0% CPU, the second will show the calculated value.
    # We set a very short interval for tests.
    OUTPUT=$(docker run --rm \
        -e PROC_ROOT="/mock_proc" \
        -e INTERVAL=0.1 \
        -v "$current_mock_proc_dir":/mock_proc:ro \
        "$IMAGE_NAME" bash -c "/app/mood_ring.sh; sleep 0.1; /app/mood_ring.sh" 2>&1 | tail -n 1)

    echo "Captured output: $OUTPUT"

    if [[ "$OUTPUT" =~ $expected_output_regex ]]; then
        echo "PASS: Output matches expected regex."
    else
        echo "FAIL: Output does NOT match expected regex."
        echo "Expected regex: $expected_output_regex"
        echo "Actual output: $OUTPUT"
        rm -rf "$current_mock_proc_dir"
        exit 1
    fi

    rm -rf "$current_mock_proc_dir"
    echo ""
}

# Create mock files for all states in a central location
create_mock_proc_files "$MOCK_PROC_DIR/mock_data"

# Test Cases
# Note: CPU usage calculation needs two readings. The first output will be 0%.
# We run the script twice and check the second output.

# Test 1: Low CPU, Low Memory -> Calm (Blue)
run_test_case \
    "Low Load (CPU: 10%, Mem: 20%)" \
    "$MOCK_PROC_DIR/mock_data/stat_low" \
    "$MOCK_PROC_DIR/mock_data/meminfo_low" \
    "^\\033\[44m\\033\[37m System Mood: Calm \(CPU: 10%, Mem: 20%\) \\033\[0m$"

# Test 2: Moderate CPU, Low Memory -> Moderate (Yellow)
run_test_case \
    "Moderate CPU (CPU: 50%, Mem: 20%)" \
    "$MOCK_PROC_DIR/mock_data/stat_moderate" \
    "$MOCK_PROC_DIR/mock_data/meminfo_low" \
    "^\\033\[43m\\033\[30m System Mood: Moderate \(CPU: 50%, Mem: 20%\) \\033\[0m$"

# Test 3: Low CPU, Moderate Memory -> Moderate (Yellow)
run_test_case \
    "Moderate Mem (CPU: 10%, Mem: 50%)" \
    "$MOCK_PROC_DIR/mock_data/stat_low" \
    "$MOCK_PROC_DIR/mock_data/meminfo_moderate" \
    "^\\033\[43m\\033\[30m System Mood: Moderate \(CPU: 10%, Mem: 50%\) \\033\[0m$"

# Test 4: High CPU, Low Memory -> Stressed (Red)
run_test_case \
    "High CPU (CPU: 80%, Mem: 20%)" \
    "$MOCK_PROC_DIR/mock_data/stat_high" \
    "$MOCK_PROC_DIR/mock_data/meminfo_low" \
    "^\\033\[41m\\033\[37m System Mood: Stressed \(CPU: 80%, Mem: 20%\) \\033\[0m$"

# Test 5: Low CPU, High Memory -> Stressed (Red)
run_test_case \
    "High Mem (CPU: 10%, Mem: 90%)" \
    "$MOCK_PROC_DIR/mock_data/stat_low" \
    "$MOCK_PROC_DIR/mock_data/meminfo_high" \
    "^\\033\[41m\\033\[37m System Mood: Stressed \(CPU: 10%, Mem: 90%\) \\033\[0m$"

# Test 6: Moderate CPU, Moderate Memory -> Moderate (Yellow)
run_test_case \
    "Moderate Load (CPU: 50%, Mem: 50%)" \
    "$MOCK_PROC_DIR/mock_data/stat_moderate" \
    "$MOCK_PROC_DIR/mock_data/meminfo_moderate" \
    "^\\033\[43m\\033\[30m System Mood: Moderate \(CPU: 50%, Mem: 50%\) \\033\[0m$"

# Test 7: High CPU, High Memory -> Stressed (Red)
run_test_case \
    "High Load (CPU: 80%, Mem: 90%)" \
    "$MOCK_PROC_DIR/mock_data/stat_high" \
    "$MOCK_PROC_DIR/mock_data/meminfo_high" \
    "^\\033\[41m\\033\[37m System Mood: Stressed \(CPU: 80%, Mem: 90%\) \\033\[0m$"

echo "All tests passed!"
