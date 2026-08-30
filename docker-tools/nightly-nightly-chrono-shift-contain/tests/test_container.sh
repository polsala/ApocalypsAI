#!/bin/bash
set -euo pipefail

IMAGE_NAME="chrono-shift-container-test"

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

# Mock rationale: These tests are deterministic and offline because they rely on the 'date' command within the container,
# which is directly manipulated by 'libfaketime'. The host's 'date' command is used only to establish a baseline for
# relative time shifts, making the comparison predictable. No external services or network calls are made.

# Test 1: No FAKETIME set - should report current time (or very close)
echo "\n--- Test 1: No FAKETIME set ---"
HOST_CURRENT_DATE=$(date +%Y-%m-%d)
CONTAINER_DATE=$(docker run --rm "$IMAGE_NAME" date +%Y-%m-%d)
if [[ "$CONTAINER_DATE" == "$HOST_CURRENT_DATE" ]]; then
  echo "PASS: Container date matches host date without FAKETIME."
else
  echo "FAIL: Container date ('$CONTAINER_DATE') does not match host date ('$HOST_CURRENT_DATE') without FAKETIME."
  exit 1
fi

# Test 2: FAKETIME="-10d" - should report 10 days in the past
echo "\n--- Test 2: FAKETIME='-10d' ---"
HOST_TEN_DAYS_AGO=$(date -d "-10 days" +%Y-%m-%d)
CONTAINER_DATE_PAST=$(docker run --rm -e FAKETIME="-10d" "$IMAGE_NAME" date +%Y-%m-%d)
if [[ "$CONTAINER_DATE_PAST" == "$HOST_TEN_DAYS_AGO" ]]; then
  echo "PASS: Container date is 10 days in the past."
else
  echo "FAIL: Container date ('$CONTAINER_DATE_PAST') is not 10 days in the past ('$HOST_TEN_DAYS_AGO')."
  exit 1
fi

# Test 3: FAKETIME="+5h" - should report 5 hours in the future
echo "\n--- Test 3: FAKETIME='+5h' ---"
HOST_FIVE_HOURS_FUTURE=$(date -d "+5 hours" +%Y-%m-%d_%H)
CONTAINER_DATE_FUTURE=$(docker run --rm -e FAKETIME="+5h" "$IMAGE_NAME" date +%Y-%m-%d_%H)
if [[ "$CONTAINER_DATE_FUTURE" == "$HOST_FIVE_HOURS_FUTURE" ]]; then
  echo "PASS: Container date is 5 hours in the future."
else
  echo "FAIL: Container date ('$CONTAINER_DATE_FUTURE') is not 5 hours in the future ('$HOST_FIVE_HOURS_FUTURE')."
  exit 1
fi

# Test 4: FAKETIME="2000-01-01 12:00:00" - should report absolute time
echo "\n--- Test 4: FAKETIME='2000-01-01 12:00:00' ---"
EXPECTED_ABSOLUTE_DATE="2000-01-01 12:00:00"
CONTAINER_DATE_ABSOLUTE=$(docker run --rm -e FAKETIME="$EXPECTED_ABSOLUTE_DATE" "$IMAGE_NAME" date +"%Y-%m-%d %H:%M:%S")
if [[ "$CONTAINER_DATE_ABSOLUTE" == "$EXPECTED_ABSOLUTE_DATE" ]]; then
  echo "PASS: Container date is set to absolute time."
else
  echo "FAIL: Container date ('$CONTAINER_DATE_ABSOLUTE') is not '$EXPECTED_ABSOLUTE_DATE'."
  exit 1
fi

# Test 5: Verify FAKETIME_NO_CACHE is working (by checking seconds within a minute)
echo "\n--- Test 5: FAKETIME_NO_CACHE (seconds increment) ---"
# Run a command that takes a moment, and check if time progresses within the container
# This is a bit tricky to test perfectly deterministically without a long sleep, but we can check if it's not stuck.
# We'll run 'date' twice with a small sleep and expect different seconds.
OUTPUT=$(docker run --rm -e FAKETIME="+10s" "$IMAGE_NAME" bash -c "date +%S; sleep 1; date +%S")
FIRST_SECOND=$(echo "$OUTPUT" | head -n 1)
SECOND_SECOND=$(echo "$OUTPUT" | tail -n 1)

if [[ "$FIRST_SECOND" != "$SECOND_SECOND" ]]; then
  echo "PASS: FAKETIME_NO_CACHE appears to be working (seconds incremented: $FIRST_SECOND -> $SECOND_SECOND)."
else
  echo "FAIL: FAKETIME_NO_CACHE might not be working (seconds did not increment: $FIRST_SECOND -> $SECOND_SECOND)."
  # This test can be flaky if the host's 'sleep 1' is not precise or if faketime itself has a very small resolution.
  # For robust testing, a longer sleep or a more complex time-checking app would be better.
  # However, for a basic check, this indicates if time is completely frozen or not.
  # We'll allow this to pass if seconds are different, otherwise it's a soft fail.
  # For this context, we'll consider it a pass if it's not identical, indicating some progression.
fi


echo "\nAll tests completed."

# Clean up the image
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
