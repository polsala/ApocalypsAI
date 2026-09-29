#!/bin/bash

set -euo pipefail

TARGET_CONTAINER=""
SCENARIO=""
DURATIONS=""
INTENSITY=""

usage() {
    echo "Usage: $0 --target-container <container_name_or_id> --scenario <scenario_name> --duration <seconds> [--intensity <value>]"
    echo "Scenarios: cpu-starvation, memory-starvation, network-latency, network-packet-loss, process-kill, filesystem-corruption"
    exit 1
}

while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        --target-container)
        TARGET_CONTAINER="$2"
        shift # past argument
        shift # past value
        ;;
        --scenario)
        SCENARIO="$2"
        shift # past argument
        shift # past value
        ;;
        --duration)
        DURATION="$2"
        shift # past argument
        shift # past value
        ;;
        --intensity)
        INTENSITY="$2"
        shift # past argument
        shift # past value
        ;;
        *)
        usage
        ;;
    esac
done

if [ -z "$TARGET_CONTAINER" ] || [ -z "$SCENARIO" ] || [ -z "$DURATION" ]; then
    usage
fi

# Ensure docker.sock is mounted for docker commands to work inside the container
if [ ! -S /var/run/docker.sock ]; then
    echo "Error: Docker socket not found at /var/run/docker.sock. Please mount it when running the container."
    exit 1
fi

echo "Initiating chaos scenario: '$SCENARIO' on container '$TARGET_CONTAINER' for $DURATION seconds with intensity '$INTENSITY'"

# Helper function to execute commands inside the target container
exec_in_container() {
    docker exec "$TARGET_CONTAINER" "$@"
}

case "$SCENARIO" in
    cpu-starvation)
        if [ -z "$INTENSITY" ]; then INTENSITY=80; fi
        echo "Injecting CPU starvation..."

        # Use stress-ng to consume CPU
        # The 'docker exec' command will run in the foreground, blocking until stress-ng finishes or is killed.
        # To make it run for a duration, we'll use a subshell and kill it after the duration.
        (exec_in_container stress-ng --cpu 0 --timeout ${DURATION}s --metrics-brief) &
        STRESS_PID=$!
        sleep $DURATION
        echo "Stopping CPU starvation..."
        docker exec "$TARGET_CONTAINER" pkill stress-ng || true
        wait $STRESS_PID 2>/dev/null || true
        ;;

    memory-starvation)
        if [ -z "$INTENSITY" ]; then INTENSITY=80; fi
        echo "Injecting Memory starvation..."

        # Use stress-ng to consume memory
        (exec_in_container stress-ng --vm 1 --vm-bytes ${INTENSITY}% --timeout ${DURATION}s --metrics-brief) &
        STRESS_PID=$!
        sleep $DURATION
        echo "Stopping Memory starvation..."
        docker exec "$TARGET_CONTAINER" pkill stress-ng || true
        wait $STRESS_PID 2>/dev/null || true
        ;;

    network-latency)
        if [ -z "$INTENSITY" ]; then INTENSITY=100; fi # ms
        echo "Injecting Network Latency ($INTENSITY ms)..."
        # Get the network interface of the container
        # This is a simplified approach; a more robust solution might inspect network namespaces.
        # For simplicity, we assume the primary interface is eth0 or similar.
        # We'll use tc to add latency to all outgoing traffic.
        # Note: This requires the container to have 'tc' installed and appropriate permissions.
        # A more robust solution would involve running this script *within* the container or using a sidecar.
        # For this example, we'll assume the target container has 'tc' and we're targeting its primary interface.
        # This is a simplification and might not work in all network configurations.
        # A better approach for real-world scenarios would be to use a tool like Toxiproxy or Chaos Mesh.
        # For demonstration purposes, we'll simulate the command execution.
        echo "Simulating: docker exec $TARGET_CONTAINER tc qdisc add dev eth0 root netem delay ${INTENSITY}ms"
        # In a real scenario, you'd execute the above command.
        # For testing, we'll just sleep and then simulate cleanup.
        sleep $DURATION
        echo "Simulating: docker exec $TARGET_CONTAINER tc qdisc del dev eth0 root netem delay ${INTENSITY}ms || true"
        ;;

    network-packet-loss)
        if [ -z "$INTENSITY" ]; then INTENSITY=10; fi # %
        echo "Injecting Network Packet Loss ($INTENSITY%)..."
        echo "Simulating: docker exec $TARGET_CONTAINER tc qdisc add dev eth0 root netem loss ${INTENSITY}%"
        sleep $DURATION
        echo "Simulating: docker exec $TARGET_CONTAINER tc qdisc del dev eth0 root netem loss ${INTENSITY}% || true"
        ;;

    process-kill)
        echo "Injecting random process kill..."
        # Kill a random process (excluding essential system processes)
        # This is a very crude way to kill processes. A more sophisticated approach would be needed.
        # We'll pick a random PID and kill it.
        # This command might fail if no suitable processes are found or if permissions are insufficient.
        echo "Simulating: docker exec $TARGET_CONTAINER sh -c 'ps -eo pid --no-headers | grep -v "^ *1 $" | grep -v "^ *[0-9]* " | shuf -n 1 | xargs -r kill -9 || true'"
        # For demonstration, we'll just sleep for a short duration and assume a kill happened.
        sleep 5 # Simulate a single kill attempt
        echo "Random process kill simulated."
        ;;

    filesystem-corruption)
        echo "WARNING: Filesystem corruption is destructive! Use with extreme caution."
        if [ -z "$INTENSITY" ]; then INTENSITY=10; fi # Probability of corrupting a file
        echo "Simulating filesystem corruption (probability: ${INTENSITY}%)..."
        # This is a highly dangerous operation. We'll simulate the command execution.
        # In a real scenario, you'd need to identify target files and use tools like 'shred'.
        # Example: Find files and shred them with a certain probability.
        echo "Simulating: docker exec $TARGET_CONTAINER find /app -type f -print0 | xargs -0 sh -c 'for f; do if (( RANDOM % 100 < ${INTENSITY} )); then shred -n 1 -u "$f"; echo "Corrupted $f"; fi; done' _"
        sleep $DURATION
        echo "Filesystem corruption simulation complete."
        ;;

    *)
        echo "Unknown scenario: $SCENARIO"
        usage
        ;;
esac

echo "Chaos scenario finished."
