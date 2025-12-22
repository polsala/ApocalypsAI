#!/usr/bin/env bash
set -euo pipefail

# Create temporary directory for mock ssh
tmpdir=$(mktemp -d)
MOCK_LOG=\"$tmpdir/ssh.log\"
export MOCK_LOG

# Mock ssh script
cat > \"$tmpdir/mock_ssh\" <<'EOF'
#!/usr/bin/env bash

echo \"ssh called with args: $@\" >> \"$MOCK_LOG\"
# Simulate long-running SSH process
while true; do sleep 1; done
EOF
chmod +x \"$tmpdir/mock_ssh\"

# Prepend mock directory to PATH
export PATH=\"$tmpdir:$PATH\"

# Path to the utility
UTIL=\"./src/main.sh\"

# Test 1: Basic tunnel creation
$UTIL -h example.com -l 2222 -r 22
output=$?
# Check exit status
if [[ $output -ne 0 ]]; then
  echo \"Test 1 failed: exit status $output\"
  exit 1
fi

# Verify mock ssh was called with correct arguments
expected=\"ssh called with args: -N -L 2222:localhost:22 example.com\"
if ! grep -q \"$expected\" \"$MOCK_LOG\"; then
  echo \"Test 1 failed: expected ssh call not found\"
  exit 1
fi

# Test 2: Command exit status propagation
MOCK_LOG=\"$tmpdir/ssh.log\"  # reset log
export MOCK_LOG
$UTIL -h example.com -l 2222 -r 22 -c \"bash -c 'exit 42'\"
cmd_status=$?
if [[ $cmd_status -ne 42 ]]; then
  echo \"Test 2 failed: expected exit status 42, got $cmd_status\"
  exit 1
fi

echo \"All tests passed\"
