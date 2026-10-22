#!/bin/bash
set -euo pipefail

IMAGE_NAME="nightly-chrono-sync-beacon"
TARGET_CONTAINER_NAME="test-chrono-target"
PAST_TIME="2000-01-01 00:00:00 UTC" # A clearly past time for deterministic testing

echo "--- Building Chrono-Sync Beacon image ---"
docker build -t "$IMAGE_NAME" .

echo "--- Starting target container for testing ---"
docker run -d --name "$TARGET_CONTAINER_NAME" busybox sleep 3600

# Mock rationale: Manually setting the target container's time to a known past value
# to simulate clock drift and provide a deterministic starting point for the test.
echo "--- Setting target container time to a past date ($PAST_TIME) ---"
docker exec "$TARGET_CONTAINER_NAME" date -u -s "$PAST_TIME"

echo "--- Verifying target container's initial time ---"
INITIAL_TARGET_TIME=$(docker exec "$TARGET_CONTAINER_NAME" date -u)
echo "Initial time in $TARGET_CONTAINER_NAME: $INITIAL_TARGET_TIME"
# Check if the initial time contains the year 2000, indicating it was set correctly.
if [[ "$INITIAL_TARGET_TIME" != *"Jan 1 00:00:00 UTC 2000"* ]]; then
    echo "ERROR: Initial time not set correctly. Expected 2000-01-01."
    docker stop "$TARGET_CONTAINER_NAME" &>/dev/null || true
    docker rm "$TARGET_CONTAINER_NAME" &>/dev/null || true
    exit 1
fi

echo "--- Running Chrono-Sync Beacon utility ---"
# Get host's current time *before* running the utility for comparison.
# This establishes a time window for the synchronization.
HOST_START_TIME_EPOCH=$(date +%s)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "$IMAGE_NAME" "$TARGET_CONTAINER_NAME"

echo "--- Verifying target container's time after sync ---"
SYNCED_TARGET_TIME_STR=$(docker exec "$TARGET_CONTAINER_NAME" date -u +"%Y-%m-%d %H:%M:%S")
SYNCED_TARGET_TIME_EPOCH=$(date -d "$SYNCED_TARGET_TIME_STR UTC" +%s)
HOST_END_TIME_EPOCH=$(date +%s) # Get host's current time *after* running the utility

echo "Synced time in $TARGET_CONTAINER_NAME: $SYNCED_TARGET_TIME_STR"
echo "Host time range during sync: $(date -d "@$HOST_START_TIME_EPOCH" -u +"%Y-%m-%d %H:%M:%S") to $(date -d "@$HOST_END_TIME_EPOCH" -u +"%Y-%m-%d %H:%M:%S")"

# Allow a small window (e.g., 15 seconds) for execution time and minor system clock variations.
# The synced time should be within this window relative to the host's time when the utility ran.
TIME_DIFF=$(( SYNCED_TARGET_TIME_EPOCH - HOST_START_TIME_EPOCH ))
if (( TIME_DIFF >= -5 && TIME_DIFF <= (HOST_END_TIME_EPOCH - HOST_START_TIME_EPOCH + 5) )); then
    echo "Test passed: Target container time is synchronized within an acceptable range."
else
    echo "Test failed: Target container time ($SYNCED_TARGET_TIME_STR) is not synchronized with host time."
    echo "Expected time to be within ~5s of host's execution window (from $HOST_START_TIME_EPOCH to $HOST_END_TIME_EPOCH)."
    exit 1
fi

echo "--- Cleaning up ---"
docker stop "$TARGET_CONTAINER_NAME" &>/dev/null || true
docker rm "$TARGET_CONTAINER_NAME" &>/dev/null || true

echo "All tests passed for Chrono-Sync Beacon!"
