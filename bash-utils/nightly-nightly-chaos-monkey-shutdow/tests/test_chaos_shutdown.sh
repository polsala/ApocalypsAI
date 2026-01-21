#!/bin/bash

set -euo pipefail

# Mock rationale: Avoid actual systemctl calls during testing.

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$TEST_DIR/../src"

# Create mock systemctl
MOCK_DIR=$(mktemp -d)
export PATH="$MOCK_DIR:$PATH"

MOCK_SYSTEMCTL="$MOCK_DIR/systemctl"
cat << 'EOF' > "$MOCK_SYSTEMCTL"
#!/bin/bash
SERVICE_NAME="$2"
ACTION="$1"
echo "Mock systemctl: $ACTION $SERVICE_NAME" >&2
if [[ "$SERVICE_NAME" == "invalid-service" ]]; then
  exit 1
fi
exit 0
EOF

chmod +x "$MOCK_SYSTEMCTL"

# Test graceful shutdown
output=$("$SRC_DIR/chaos_shutdown.sh" "nginx" 2>&1)
if [[ "$output" != *"Gracefully stopping service: nginx"* ]]; then
  echo "FAIL: Graceful shutdown test failed"
  exit 1
fi

# Test force shutdown
output=$("$SRC_DIR/chaos_shutdown.sh" "nginx" "--force" 2>&1)
if [[ "$output" != *"Forcefully stopping service: nginx"* ]]; then
  echo "FAIL: Force shutdown test failed"
  exit 1
fi

# Test invalid service
output=$("$SRC_DIR/chaos_shutdown.sh" "invalid-service" 2>&1 || true)
if [[ "$output" != *"Failed to stop invalid-service"* ]]; then
  echo "FAIL: Invalid service test failed"
  exit 1
fi

# Cleanup
rm -rf "$MOCK_DIR"

echo "All tests passed."
