#!/bin/bash

set -euo pipefail

# Mock Docker commands

# Mock docker exec to capture commands and arguments
docker_exec_mock() {
    echo "MOCK_DOCKER_EXEC: $@" >> /tmp/mock_docker_exec.log
    # Simulate success for most commands, or specific behavior if needed
    if [[ "$@" == *"pkill stress-ng"* ]] || [[ "$@" == *"tc qdisc del"* ]] || [[ "$@" == *"kill -9"* ]] || [[ "$@" == *"shred"* ]]; then
        return 0 # Simulate successful cleanup/kill
    elif [[ "$@" == *"ps -eo pid"* ]]; then
        echo "1234\n5678\n9012" # Mock PIDs
        return 0
    elif [[ "$@" == *"find /app"* ]]; then
        echo "/app/file1.txt\n/app/subdir/file2.log"
        return 0
    fi
    return 0
}

# Mock docker run to capture commands and arguments
docker_run_mock() {
    echo "MOCK_DOCKER_RUN: $@" >> /tmp/mock_docker_run.log
    # Simulate the container running and the script executing within it
    if [[ "$@" == *"container-chaos-gen"* ]]; then
        # Simulate the script running inside the container
        # We need to parse the arguments passed to the script itself
        local script_args=$(echo "$@" | sed -n 's/.*container-chaos-gen \(.*\)/\1/p')
        # Execute the script with mocked docker exec
        # We need to temporarily replace docker exec with our mock
        local original_docker_exec="docker_exec_mock"
        local original_docker_run="docker_run_mock"
        local original_sleep="sleep"
        local original_pkill="pkill"
        local original_tc="tc"
        local original_shuf="shuf"
        local original_find="find"
        local original_xargs="xargs"
        local original_shred="shred"

        # Mocking internal commands used by chaos-generator.sh
        alias docker_exec='docker_exec_mock'
        alias sleep='echo "MOCK_SLEEP: $@" >> /tmp/mock_docker_exec.log; return 0'
        alias pkill='echo "MOCK_PKILL: $@" >> /tmp/mock_docker_exec.log; return 0'
        alias tc='echo "MOCK_TC: $@" >> /tmp/mock_docker_exec.log; return 0'
        alias shuf='echo "MOCK_SHUF: $@" >> /tmp/mock_docker_exec.log; echo "1234"'
        alias find='echo "MOCK_FIND: $@" >> /tmp/mock_docker_exec.log; echo "/app/file1.txt\n/app/subdir/file2.log"
        alias xargs='echo "MOCK_XARGS: $@" >> /tmp/mock_docker_exec.log; return 0'
        alias shred='echo "MOCK_SHRED: $@" >> /tmp/mock_docker_exec.log; return 0'

        # Execute the script with the provided arguments
        bash chaos-generator.sh $script_args

        # Restore aliases
        unalias docker_exec
        unalias sleep
        unalias pkill
        unalias tc
        unalias shuf
        unalias find
        unalias xargs
        unalias shred

        return 0
    fi
    return 1
}

# Mock docker socket check
mock_docker_socket() {
    echo "MOCK_DOCKER_SOCKET: $@" >> /tmp/mock_docker_exec.log
    return 0 # Simulate docker.sock is available
}

# Helper to clean up mock logs
cleanup_mocks() {
    rm -f /tmp/mock_docker_exec.log /tmp/mock_docker_run.log
}

# --- Test Cases ---

# Test 1: CPU Starvation
test_cpu_starvation() {
    echo "Running test_cpu_starvation..."
    cleanup_mocks
    export -f docker_exec_mock
    export -f docker_run_mock
    export -f mock_docker_socket
    alias docker_exec='docker_exec_mock'
    alias docker_run='docker_run_mock'
    alias docker='echo "MOCK_DOCKER: $@" >> /tmp/mock_docker_exec.log'

    # Simulate running the container with the chaos generator
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen --target-container my-app --scenario cpu-starvation --duration 30 --intensity 80

    # Assertions
    grep -q "MOCK_DOCKER_EXEC: stress-ng --cpu 0 --timeout 30s --metrics-brief" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: pkill stress-ng" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: sleep 30" /tmp/mock_docker_exec.log

    unalias docker_exec docker_run docker
    echo "test_cpu_starvation PASSED"
}

# Test 2: Network Latency
test_network_latency() {
    echo "Running test_network_latency..."
    cleanup_mocks
    export -f docker_exec_mock
    export -f docker_run_mock
    export -f mock_docker_socket
    alias docker_exec='docker_exec_mock'
    alias docker_run='docker_run_mock'
    alias docker='echo "MOCK_DOCKER: $@" >> /tmp/mock_docker_exec.log'

    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen --target-container web-server --scenario network-latency --duration 60 --intensity 150

    # Assertions
    grep -q "MOCK_DOCKER_EXEC: tc qdisc add dev eth0 root netem delay 150ms" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: tc qdisc del dev eth0 root netem delay 150ms" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: sleep 60" /tmp/mock_docker_exec.log

    unalias docker_exec docker_run docker
    echo "test_network_latency PASSED"
}

# Test 3: Process Kill
test_process_kill() {
    echo "Running test_process_kill..."
    cleanup_mocks
    export -f docker_exec_mock
    export -f docker_run_mock
    export -f mock_docker_socket
    alias docker_exec='docker_exec_mock'
    alias docker_run='docker_run_mock'
    alias docker='echo "MOCK_DOCKER: $@" >> /tmp/mock_docker_exec.log'

    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen --target-container worker-node --scenario process-kill --duration 10

    # Assertions
    grep -q "MOCK_DOCKER_EXEC: ps -eo pid --no-headers" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: shuf -n 1" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: xargs -r kill -9" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: sleep 5" /tmp/mock_docker_exec.log

    unalias docker_exec docker_run docker
    echo "test_process_kill PASSED"
}

# Test 4: Filesystem Corruption (Simulated)
test_filesystem_corruption() {
    echo "Running test_filesystem_corruption..."
    cleanup_mocks
    export -f docker_exec_mock
    export -f docker_run_mock
    export -f mock_docker_socket
    alias docker_exec='docker_exec_mock'
    alias docker_run='docker_run_mock'
    alias docker='echo "MOCK_DOCKER: $@" >> /tmp/mock_docker_exec.log'

    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen --target-container data-store --scenario filesystem-corruption --duration 120 --intensity 25

    # Assertions
    grep -q "MOCK_DOCKER_EXEC: find /app -type f -print0" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: xargs -0 sh -c 'for f; do if (( RANDOM % 100 < 25 )); then shred -n 1 -u \"$f\"; echo \"Corrupted $f\"; fi; done' _" /tmp/mock_docker_exec.log
    grep -q "MOCK_DOCKER_EXEC: sleep 120" /tmp/mock_docker_exec.log

    unalias docker_exec docker_run docker
    echo "test_filesystem_corruption PASSED"
}

# --- Main Test Execution ---

# Ensure the script is executable
chmod +x chaos-generator.sh

# Mock docker commands globally for the test runner
# This is a simplified approach. In a real CI, you'd use a testing framework.

# Mock docker socket check for the script itself
export -f mock_docker_socket
alias docker='echo "MOCK_DOCKER: $@" >> /tmp/mock_docker_exec.log'

# Run tests
test_cpu_starvation
test_network_latency
test_process_kill
test_filesystem_corruption

echo "All tests passed!"
