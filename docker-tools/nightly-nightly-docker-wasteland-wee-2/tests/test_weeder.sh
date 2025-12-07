# Mock docker commands for deterministic testing
# Mock rationale: Simulates Docker CLI responses without requiring real Docker daemon
MOCK_OUTPUT="$(mktemp)"

# Test 1: Basic cleanup detection
printf "$(cat << 'EOF')
# Mock docker ps -a -f status=exited
CONTAINER ID
abandoned123

# Mock docker images -f dangling=true
IMAGE
ghostimg1

# Mock docker volume ls -f dangling=true
VOLUME
orphanvol1
EOF
)
" > $MOCK_OUTPUT

# Replace real docker commands with mock
export PATH=$(dirname $MOCK_OUTPUT):$PATH
alias docker='cat $MOCK_OUTPUT'

# Run test
./src/weeder.sh --whisper | grep -q "Uprooting ghost containers" && \
  grep -q "Clearing abandoned images" && \
  grep -q "Removing rootless volumes" && \
  grep -q "Your Docker garden" && \
  echo "✅ Test passed" || echo "❌ Test failed"

# Cleanup
rm $MOCK_OUTPUT
unalias docker
