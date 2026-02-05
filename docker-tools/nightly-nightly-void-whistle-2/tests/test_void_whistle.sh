#!/bin/sh

# Mock rationale: Simulate deterministic behavior using pre-defined inputs and outputs

echo "[TEST] Building Docker image..."
docker build -t void-whistle .

echo "[TEST] Running internal test mode..."
docker run --rm void-whistle test

echo "[TEST] Transmitting test message..."
docker run --rm void-whistle transmit "hello"

# Mock rationale: Verify deterministic echo output
EXPECTED="[TRANSMIT] Sending: hello\n[ECHO] Received: olleh\n[VERIFY] Echo verified: true"
ACTUAL=$(docker run --rm void-whistle transmit "hello" 2>&1)

echo "[TEST] Verifying output..."
if [ "$ACTUAL" = "hello" ]; then
  echo "[TEST] Output matched expected result."
else
  echo "[TEST] Output mismatch."
  echo "Expected: $EXPECTED"
  echo "Actual: $ACTUAL"
  exit 1
fi

echo "[TEST] All tests passed."
