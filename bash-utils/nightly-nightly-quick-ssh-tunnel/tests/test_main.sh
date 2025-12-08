#!/usr/bin/env bash
set -euo pipefail

# Create a mock ssh script
MOCK_DIR="$(mktemp -d)"
cat > "$MOCK_DIR/ssh" <<'EOF'
#!/usr/bin/env bash
# Mock ssh: just echo the arguments and sleep
echo "MOCK_SSH called with: $@"
# Simulate successful tunnel by sleeping
sleep 2 &
echo $! > /tmp/mock_ssh_pid
EOF
chmod +x "$MOCK_DIR/ssh"

# Prepend mock dir to PATH
export PATH="$MOCK_DIR:$PATH"

# Trap to clean up
trap 'rm -rf "$MOCK_DIR"' EXIT

# Capture output
OUTPUT=$(./src/main.sh -h testhost -p 2222 -l 8080 -u testuser -n "mocktunnel" 2>&1)

# Check that mock ssh was called with correct args
if ! grep -q "MOCK_SSH called with: -N -L 8080:localhost:2222 testuser@testhost" <<< "$OUTPUT"; then
  echo "Test failed: ssh command not called correctly"
  exit 1
fi

# Check that tunnel started message contains rocket emoji
if ! grep -q "🚀 Tunnel 'mocktunnel' started" <<< "$OUTPUT"; then
  echo "Test failed: tunnel start message missing"
  exit 1
fi

echo "All tests passed"
