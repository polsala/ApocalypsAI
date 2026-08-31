#!/bin/bash

# Mock rationale: We cannot run actual docker commands in a CI/CD environment without a docker daemon,
# and we want deterministic, offline tests. Mocking the 'docker' command allows us to verify
# that our cleanup script calls the correct docker prune commands with the expected filters.

# --- Setup Mock Docker ---
MOCK_DOCKER_DIR=$(mktemp -d)
export PATH="$MOCK_DOCKER_DIR:$PATH"
MOCK_LOG="$MOCK_DOCKER_DIR/mock_docker.log"

# Create a mock docker executable
cat << 'EOF' > "$MOCK_DOCKER_DIR/docker"
#!/bin/bash
echo "MOCK DOCKER CALLED: $@" >> "$MOCK_LOG"
# Simulate success for prune commands
if [[ "$@" == *prune* ]]; then
    echo "Total reclaimed space: 100MB" # Simulate some output
    exit 0
fi
# For other commands, just exit 0
exit 0
EOF
chmod +x "$MOCK_DOCKER_DIR/docker"
# --- End Setup Mock Docker ---

cleanup() {
    rm -rf "$MOCK_DOCKER_DIR"
}
trap cleanup EXIT

echo "Running tests for cleanup.sh"

# Test 1: Default run (7 days, not verbose, not dry-run)
echo "Test 1: Default run"
./src/cleanup.sh > /dev/null # Suppress stdout for cleaner test output
if grep -q "MOCK DOCKER CALLED: container prune -f --filter \"until=7d\"" "$MOCK_LOG" && \
   grep -q "MOCK DOCKER CALLED: image prune -f --filter \"until=7d\"" "$MOCK_LOG" && \
   grep -q "MOCK DOCKER CALLED: volume prune -f --filter \"until=7d\"" "$MOCK_LOG" && \
   grep -q "MOCK DOCKER CALLED: network prune -f --filter \"until=7d\"" "$MOCK_LOG"; then
    echo "  PASS: Default prune commands with 7d filter were called."
else
    echo "  FAIL: Default prune commands were NOT called as expected."
    cat "$MOCK_LOG"
    exit 1
fi
rm "$MOCK_LOG" # Clear log for next test
echo ""

# Test 2: Custom days-old
echo "Test 2: Custom days-old (3 days)"
./src/cleanup.sh --days-old 3 > /dev/null
if grep -q "MOCK DOCKER CALLED: container prune -f --filter \"until=3d\"" "$MOCK_LOG" && \
   grep -q "MOCK DOCKER CALLED: image prune -f --filter \"until=3d\"" "$MOCK_LOG" && \
   grep -q "MOCK DOCKER CALLED: volume prune -f --filter \"until=3d\"" "$MOCK_LOG" && \
   grep -q "MOCK DOCKER CALLED: network prune -f --filter \"until=3d\"" "$MOCK_LOG"; then
    echo "  PASS: Custom days-old filter (3d) was applied."
else
    echo "  FAIL: Custom days-old filter was NOT applied."
    cat "$MOCK_LOG"
    exit 1
fi
rm "$MOCK_LOG"
echo ""

# Test 3: Dry-run mode
echo "Test 3: Dry-run mode"
./src/cleanup.sh --dry-run > /dev/null
if grep -q "\[DRY RUN\] Would execute: docker container prune -f --filter \"until=7d\"" "$MOCK_LOG" && \
   grep -q "\[DRY RUN\] Would execute: docker image prune -f --filter \"until=7d\"" "$MOCK_LOG" && \
   grep -q "\[DRY RUN\] Would execute: docker volume prune -f --filter \"until=7d\"" "$MOCK_LOG" && \
   grep -q "\[DRY RUN\] Would execute: docker network prune -f --filter \"until=7d\"" "$MOCK_LOG"; then
    echo "  PASS: Dry-run messages were logged, and commands were not executed."
else
    echo "  FAIL: Dry-run mode did not behave as expected."
    cat "$MOCK_LOG"
    exit 1
fi
rm "$MOCK_LOG"
echo ""

# Test 4: Verbose mode
echo "Test 4: Verbose mode"
OUTPUT=$(./src/cleanup.sh --verbose)
if echo "$OUTPUT" | grep -q "🧹 ApocalypsAI Dust Bunny Sweeper: Starting the great Docker Dust Bunny Sweep!" && \
   echo "$OUTPUT" | grep -q "🧹 ApocalypsAI Dust Bunny Sweeper: Sweeping stopped containers..."; then
    echo "  PASS: Verbose output was generated."
else
    echo "  FAIL: Verbose output was NOT generated."
    echo "$OUTPUT"
    exit 1
fi
rm "$MOCK_LOG"
echo ""

# Test 5: Environment variable DAYS_OLD
echo "Test 5: Environment variable DAYS_OLD (1 day)"
DAYS_OLD=1 ./src/cleanup.sh > /dev/null
if grep -q "MOCK DOCKER CALLED: container prune -f --filter \"until=1d\"" "$MOCK_LOG"; then
    echo "  PASS: DAYS_OLD environment variable was respected."
else
    echo "  FAIL: DAYS_OLD environment variable was NOT respected."
    cat "$MOCK_LOG"
    exit 1
fi
rm "$MOCK_LOG"
echo ""

echo "All tests passed!"
