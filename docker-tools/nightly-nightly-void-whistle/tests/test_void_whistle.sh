#!/bin/sh

# Mock rationale: We can't play sounds in CI, so we test entrypoint logic only.

echo "== Testing nightly-void-whistle =="

docker build -t test-void-whistle .

# Test default sound
OUTPUT=$(docker run --rm test-void-whistle 2>&1)
if echo "$OUTPUT" | grep -q "Playing sound: rift"; then
  echo "✅ Default sound test passed"
else
  echo "❌ Default sound test failed"
  exit 1
fi

# Test specific sound
OUTPUT=$(docker run --rm test-void-whistle tear 2>&1)
if echo "$OUTPUT" | grep -q "Playing sound: tear"; then
  echo "✅ Specific sound test passed"
else
  echo "❌ Specific sound test failed"
  exit 1
fi

# Test unknown sound
OUTPUT=$(docker run --rm test-void-whistle unknown 2>&1)
if echo "$OUTPUT" | grep -q "Unknown sound type: unknown"; then
  echo "✅ Unknown sound test passed"
else
  echo "❌ Unknown sound test failed"
  exit 1
fi

echo "== All tests passed =="
